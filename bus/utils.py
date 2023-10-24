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
    Utilidades utilizadas a lo largo de todo el programa. Incluye funciones
    como buscar una parada o una línea y otras funciones relacionadas con la
    información en tiempo real sobre los buses: buses para una parada, buses
    para una línea, geojson con las paradas para una línea o salidas de una línea.
"""
import datetime
import json
import math
import requests
from bus import cache

# Buscar una línea en la lista de líneas y devolverla
def encontrar_linea(id, datos):
    for linea in datos['lineas']:
        if linea['id'] == id:
            return linea

# Buscar una parada en la lista de paradas y devolverla
def encontrar_parada(id, datos):
    for parada in datos['paradas']:
        if parada['id'] == id:
            return parada

# Datos actuales de los buses para una parada
@cache.memoize(20)
def buses_parada(id_parada, jlineas):
    try:
        parada = peticion(id_parada, 'parada')
    except:
        return 429
    if not 'lineas' in parada['buses']:
        return {'error': 'No hay buses para esta parada'}
    for linea in range(len(parada['buses']['lineas'])):
        parada['buses']['lineas'][linea]['linea'] = encontrar_linea(parada['buses']['lineas'][linea]['linea'], jlineas)
    return parada

# Datos actuales de las posiciones de los buses en una línea
@cache.memoize(20)
def buses_linea(linea):
    try:
        return peticion(linea, 'linea')
    except:
        return 429

# GeoJSON con las paradas de una línea
def geojson_linea(id, rutas):
    features = []
    for linea in rutas['lineas']:
        if linea['id'] == id:
            for sentido in linea['paradas'].keys():
                for parada in linea['paradas'][sentido]:
                    coordenadas = parada['coords'] if parada['osmcoords'] == [] else parada['osmcoords']
                    features.append({
                        'type': 'Feature',
                        'properties': {
                            'name': parada['nombre'],
                            'popupContent': parada['nombre']
                        },
                        'geometry': {
                            'type': 'Point',
                            'coordinates': coordenadas
                        }
                    })
    geojson = {'type': 'FeatureCollection', 'features': features}
    return f'var paradas = {json.dumps(geojson)};'
                        

# Salidas de una línea
def salidas(id, fecha):
    base = 'https://itranvias.com/queryitr_v3.php?func='
    func = '8'
    dato = str(id)
    fecha = str(fecha)
    ip = '192.168.20.'+str(math.ceil(id/100))
    try:
        horas = requests.get(f'{base}{func}&dato={dato}&fecha={fecha}', headers={'X-Forwarded-For': ip}).json()
    except:
        return 429
    respuesta = {'ida': [], 'vuelta': []}
    for x in horas['servicios'][0]['ida']:
        respuesta['ida'].append(f'{str(x)[:-2]}:{str(x)[-2:]}')
    for x in horas['servicios'][0]['vuelta']:
        respuesta['vuelta'].append(f'{str(x)[:-2]}:{str(x)[-2:]}')
    return respuesta

def peticion(dato, tipo):
    if tipo == 'parada':
        func = 0
        # Convertir la parada a una ip. ej: parada 1=192.168.0.1; parada 256=192.168.1.1; parada 300=192.168.1.5
        # 192.168.1.0//192.168.255.255 -> dato/256, truncar (=x). dato-(256*x) (=y) => 192.168.x.y
        x = math.trunc(dato/256)+1
        y = dato-256*(x-1)
        ip = '192.168.'+str(x)+'.'+str(y)
    elif tipo == 'linea':
        func = 2
        # Convertir la línea en una ip. ej: línea 301=192.168.0.4
        # 192.168.0.0//192.168.0.255 -> dato/100, aproximar hacia arriba
        i = math.ceil(dato/100)
        ip = '192.168.0.'+str(i)
    base = 'https://itranvias.com/queryitr_v3.php?func='
    return requests.get(base+str(func)+'&dato='+str(dato), headers={'X-Forwarded-For': ip}).json()
