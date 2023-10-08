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
import json
import requests
import time
from bus.utils import encontrar_linea, encontrar_parada

# Actualizar los datos a partir de la URL del servidor y el directorio del resultado
def actualizar(url, dirs):
    with open(dirs['queryitr']) as f:
        respuesta = json.load(f)['iTranvias']['actualizacion']

    # Cargar los datos de openstreetmap
    with open(dirs['osm']) as archivo:
        osm = json.load(archivo)

    # Generar los archivos y cargar los datos
    jlineas = json_lineas(respuesta['lineas'], dirs['lineas'])
    jparadas = json_paradas(respuesta['paradas'], dirs['paradas'], osm, jlineas)
    jrutas = json_rutas(respuesta['lineas'], dirs['rutas'], jparadas)
    geojson(jparadas, dirs['geojson'])

    return jlineas, jparadas, jrutas    # Devolver los datos actualizados

# Generar un JSON con todas las líneas. (id, nombre, origen, destino, color)
def json_lineas(datos, dir):
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
    with open(dir, 'w') as archivo:
        archivo.write(json.dumps({'lineas': lineas}))

    return {'lineas': lineas}   # Devolver el resultado


# Generar un JSON con todas las paradas. (id, nombre, propiedades: [
# pavimento, banco, marquesina, papelera, iluminada], líneas: [id, nombre,
# color], coordenadas, coordenadas de OSM)
def json_paradas(datos, dir, osm, jlineas):
    # Buscar un elemento en los datos de OSM
    def find(ref):
        for feature in osm['features']: # Iterar por todos los elementos
            if 'ref' in feature['properties'] and feature['properties']['ref'] == str(ref):
                detalles = {}
                propiedades = ['tactile_paving', 'bench', 'shelter', 'bin', 'lit']  # Propiedades que se guardarán
                for propiedad in propiedades:
                    if propiedad in feature['properties'] and feature['properties'][propiedad] == 'yes':
                        detalles[propiedad] = True
                    elif propiedad in feature['properties'] and feature['properties'][propiedad] == 'no':
                        detalles[propiedad] = False
                    else:
                        detalles[propiedad] = None
                return detalles, feature['geometry']['coordinates']
        # Si se llega a este punto es porque no existe la parada en OSM
        # o no se pudo relacionar correctamente, devolver elementos vacíos
        return None, None

    # Generar los datos de las paradas
    paradas = []
    for parada in datos:    # Para cada parada
        if not parada['enlaces'] == []:  # Evitar las paradas que no tienen enlaces
            detalles, osmcoords = find(parada['id'])    # Recopilar los datos de OSM
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
                'osmcoords': osmcoords
            })
    
    # Guardar el resultado en un archivo
    with open(dir, 'w') as archivo:
        archivo.write(json.dumps({'paradas': paradas}))

    return {'paradas': paradas} # Devolver el resultado

# Generar un JSON con las paradas por las que pasa cada línea
def json_rutas(datos, dir, paradas):
    rutas = []
    for linea in datos:
        l = {'id': linea['id'], 'paradas': {'ida': [], 'vuelta': []}}
        for parada in linea['rutas'][0]['paradas']:
            l['paradas']['ida'].append(encontrar_parada(parada, paradas))
        for parada in linea['rutas'][1]['paradas']:
            l['paradas']['vuelta'].append(encontrar_parada(parada, paradas))
        rutas.append(l)

    # Guardar el resultado en un archivo
    with open(dir, 'w') as archivo:
        archivo.write(json.dumps({'lineas': rutas}))

    return {'lineas': rutas}    # Devolver el resultado

# Generar un GeoJSON con todas las paradas y un diálogo que enlaza a la
# parada y a las líneas que pasan por la parada
def geojson(datos, dir):
    paradas = []
    for parada in datos['paradas']:
        lineas = '<br>'
        for linea in parada['lineas']:
            # Contenido del popup del mapa
            lineas += f'<a href="./linea/{linea["id"]}" class="simbolo_linea" style="background-color: #{linea["color"]}">{linea["nombre"]}</a>'
        # Solo utilizar las coordenadas de OSM si no están vacías
        coordenadas = parada['coords'] if parada['osmcoords'] == None else parada['osmcoords']
        paradas.append({'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': f'<a href="./parada/{parada["id"]}">{parada["nombre"]}</a>{lineas}'}, 'geometry': {'type': 'Point', 'coordinates': coordenadas}})
    
    # Guardar el resultado en un archivo
    with open(dir, 'w') as archivo:
        archivo.write('var paradas = '+json.dumps({'type': 'FeatureCollection', 'features': paradas})+';')

# Descarga los datos de OSM a través de overpass y los guarda en un archivo GeoJSON
def datos_osm(dir):
    stops = ox.geometries_from_place('A Coruña, Galicia, España', {'public_transport': 'platform', 'bus': 'yes'})
    stops = stops.loc[stops.geometry.type=='Point']
    stops.to_file(dir, driver='GeoJSON')
