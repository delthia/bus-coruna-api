# bus.delthia.com - información en tiempo real del bus de Coruña
# Copyright (C) 2023  <Iago, delthia@delthia.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
    Parte del código que actualiza los datos de la aplicación. Descarga los
    datos de las paradas y las líneas y genera archivos con las paradas, las
    líneas y una relación entre ambas. También genera otros archivos con datos
    adicionales como son las tarifas o los enlaces entre líneas.
"""
from datetime import datetime, timedelta
import json
import os
import requests
from bus.utils import encontrar_linea, encontrar_parada


# Actualizar los datos a partir de la URL del
# servidor y el directorio del resultado
def actualizar(url, dirs):
    # Cargar los datos de los archivos
    def cargar_archivos(dirs):
        with open(dirs['lineas']) as lineas:
            jlineas = json.load(lineas)

        with open(dirs['paradas']) as paradas:
            jparadas = json.load(paradas)

        with open(dirs['rutas']) as rutas:
            jrutas = json.load(rutas)

        return jlineas, jparadas, jrutas

    # Si los archivos existen y hace menos de 12horas que se actualizaron
    if os.path.exists(dirs['lineas']) and \
        datetime.fromtimestamp(os.path.getmtime(dirs['lineas'])) > \
            datetime.now() - timedelta(hours=12):
        # Solo cargar los archivos
        jlineas, jparadas, jrutas = cargar_archivos(dirs)

    else:   # En caso contrario
        try:
            respuesta = requests.get(url).json()['iTranvias']['actualizacion']

            # Cargar los datos de openstreetmap
            with open(dirs['osm']) as archivo:
                osm = json.load(archivo)

            # Generar los archivos y cargar los datos
            jlineas = json_lineas(respuesta['lineas'], dirs['lineas'])
            jparadas = json_paradas(respuesta['paradas'], dirs['paradas'], osm, jlineas)
            jrutas = json_rutas(respuesta['lineas'], dirs['rutas'], jparadas)
            geojson(jparadas, dirs['geojson'])
        except:
            jlineas, jparadas, jrutas = cargar_archivos(dirs)

    return jlineas, jparadas, jrutas    # Devolver los datos actualizados


# Generar un JSON con todas las líneas. (id, nombre, origen, destino, color)
def json_lineas(datos, directorio):
    lineas = []
    for linea in datos:
        lineas.append({
            'id': linea['id'],
            'nombre': linea['lin_comer'],
            'origen': linea['nombre_orig'],
            'destino': linea['nombre_dest'],
            'color': linea['color']
        })

    # Guardar el resultado en un archivo
    with open(directorio, 'w') as archivo:
        archivo.write(json.dumps({'lineas': lineas}))

    return {'lineas': lineas}   # Devolver el resultado


# Generar un JSON con todas las paradas. (id, nombre, propiedades: [
# pavimento, banco, marquesina, papelera, iluminada], líneas: [id, nombre,
# color], coordenadas, coordenadas de OSM)
def json_paradas(datos, directorio, osm, jlineas):
    # Buscar un elemento en los datos de OSM
    def find(ref):
        for feature in osm['features']:  # Iterar por todos los elementos
            if 'ref' in feature['properties'] and \
                feature['properties']['ref'] == str(ref):
                detalles = {}
                propiedades = ['tactile_paving', 'bench', 'shelter', 'bin', 'lit']  # Propiedades que se guardarán
                for propiedad in propiedades:
                    if propiedad in feature['properties'] and feature['properties'][propiedad] == 'yes':
                        detalles[propiedad] = True
                    elif propiedad in feature['properties'] and feature['properties'][propiedad] == 'no':
                        detalles[propiedad] = False
                    else:
                        detalles[propiedad] = None
                return detalles, feature['geometry']['coordinates'], feature['properties']['osmid']
        # Si se llega a este punto es porque no existe la parada en OSM
        # o no se pudo relacionar correctamente, devolver elementos vacíos
        return None, None, None

    # Generar los datos de las paradas
    paradas = []
    for parada in datos:    # Para cada parada
        if not parada['enlaces'] == []:  # Evitar las paradas que no tienen enlaces
            detalles, osmcoords, osmid = find(parada['id'])    # Recopilar los datos de OSM
            lineas = []
            # Crear la lista de líneas que pasan por una parada
            for enlace in parada['enlaces']:
                linea = encontrar_linea(enlace, jlineas)
                lineas.append({
                    'id': linea['id'],
                    'nombre': linea['nombre'],
                    'color': linea['color']
                })
            # Añadir la parada a la lista
            paradas.append({
                'id': parada['id'],
                'nombre': parada['nombre'],
                'propiedades': detalles,
                'lineas': lineas,
                'coords': [parada['posx'], parada['posy']],
                'osmcoords': osmcoords,
                'osmid': osmid
            })

    # Guardar el resultado en un archivo
    with open(directorio, 'w') as archivo:
        archivo.write(json.dumps({'paradas': paradas}))

    return {'paradas': paradas}  # Devolver el resultado


# Generar un JSON con las paradas por las que pasa cada línea
def json_rutas(datos, directorio, paradas):
    rutas = []
    for linea in datos:
        l = {'id': linea['id'], 'paradas': {'ida': [], 'vuelta': []}}
        for parada in linea['rutas'][0]['paradas']:
            l['paradas']['ida'].append(encontrar_parada(parada, paradas))
        for parada in linea['rutas'][1]['paradas']:
            l['paradas']['vuelta'].append(encontrar_parada(parada, paradas))
        rutas.append(l)

    # Guardar el resultado en un archivo
    with open(directorio, 'w') as archivo:
        archivo.write(json.dumps({'lineas': rutas}))

    return {'lineas': rutas}    # Devolver el resultado


# Generar un GeoJSON con todas las paradas y un diálogo que enlaza a la
# parada y a las líneas que pasan por la parada
def geojson(datos, directorio):
    paradas = []
    for parada in datos['paradas']:
        lineas = '<br>'
        for linea in parada['lineas']:
            # Contenido del popup del mapa
            lineas += f'<a href="./linea/{linea["id"]}" class="simbolo_linea" style="background-color: #{linea["color"]}">{linea["nombre"]}</a>'
        # Solo utilizar las coordenadas de OSM si no están vacías
        coordenadas = parada['coords'] if parada['osmcoords'] is None else parada['osmcoords']
        paradas.append({'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': f'<a href="./parada/{parada["id"]}">{parada["nombre"]}</a>{lineas}'}, 'geometry': {'type': 'Point', 'coordinates': coordenadas}})

    # Guardar el resultado en un archivo
    with open(directorio, 'w') as archivo:
        archivo.write('var paradas = '+json.dumps({'type': 'FeatureCollection', 'features': paradas})+';')


# Descarga los datos de OSM a través de overpass y los guarda en un archivo GeoJSON
def datos_osm(directorio):
    stops = ox.geometries_from_place('A Coruña, Galicia, España', {'public_transport': 'platform', 'bus': 'yes'})
    stops = stops.loc[stops.geometry.type == 'Point']
    stops.to_file(directorio, driver='GeoJSON')
