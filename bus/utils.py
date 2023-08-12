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

import requests
import json
import math
import datetime

cache_paradas = {}  # Diccionario que almacena los datos de las paradas; {'565': [<dato>, <fecha_dato>]}
cache_lineas = {}   # Diccionario que almacena los datos de las líneas

"""
Funciones variadas. Se utilizan en el resto del código para buscar paradas, líneas, o para obtener los datos de buses y paradas
"""

# Busca una línea en la lista de líneas y la devuelve
def encontrar_linea(id, datos):
    for linea in datos['lineas']:
        if linea['id'] == id:
            return linea

# Busca una parada en la lista de paradas y la devuelve
def encontrar_parada(id, datos):
    for parada in datos['paradas']:
        if parada['id'] == id:
            return parada

# Recoge los datos actuales de los buses para una parada
def buses_parada(parada, directorio):
    try:
        dato = cache(cache_paradas, parada, 'parada')
    except:
        return 429
    with open(directorio) as a:
        lista = json.load(a)
    if not 'lineas' in dato['buses']:
        return 1111
    # Comprobar si el json de los ya contiene la  información de las paradas
    # Necesario para cuando los datos se recuperan de la caché
    if type(dato['buses']['lineas'][0]['linea']) == int:
        for linea in range(0, len(dato['buses']['lineas'])):
            dato['buses']['lineas'][linea]['linea'] = encontrar_linea(dato['buses']['lineas'][linea]['linea'], lista)
    return dato

# Recoge los datos actuales de las posiciones de los buses en el recorrido de una línea
def buses_linea(linea):
    try:
        dato = cache(cache_lineas, linea, 'linea')
    except:
        return 429
    return dato

# Recoge los datos de las posiciones de los buses de una línea y devuelve un GeoJSON con esa información
"""def geojson_buses(linea):
    try:
        dato = requests.get('http://itranvias.com/queryitr_v3.php?&func=99&mostrar=B&dato='+str(linea)).json()['mapas'][0]['buses']
    except:
        return 429
    b = []
    for sentido in range(0, len(dato)):
        for bus in range(0, len(dato[sentido]['buses'])):
            b.append({'type': 'Feature', 'properties': {'name': dato[sentido]['buses'][bus]['bus']}, 'geometry': {'type': 'Point', 'coordinates': [dato[sentido]['buses'][bus]['posx'], dato[sentido]['buses'][bus]['posy']]}})

    # return 'var buses = {"type": "FeatureCollection", "features":'+str(b)+'}'
    return '{"type": "FeatureCollection", "features":'+str(b)+'}'"""

# GeoJSON con las paradas de una línea
def geojson_linea(id, geojson):
    head = {'type': 'FeatureCollection', 'features': []}
    for linea in geojson['lineas']:
        if linea['id'] == id:
            for parada in linea['paradas']['ida']:
                if parada['osmcoords'] == []:
                    feature = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': parada['nombre']}, 'geometry': {'type': 'Point', 'coordinates': parada['coords']}}
                else:
                    feature = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': parada['nombre']}, 'geometry': {'type': 'Point', 'coordinates': parada['osmcoords']}}
                head['features'].append(feature)
            for parada in linea['paradas']['vuelta']:
                if parada['osmcoords'] == []:
                    feature = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': parada['nombre']}, 'geometry': {'type': 'Point', 'coordinates': parada['coords']}}
                else:
                    feature = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': parada['nombre']}, 'geometry': {'type': 'Point', 'coordinates': parada['osmcoords']}}
                head['features'].append(feature)
    return 'var paradas = '+json.dumps(head)+';'

# Salidas de una línea
def salidas(id, fecha):
    base = 'https://itranvias.com/queryitr_v3.php?func='
    func = '8'
    dato = str(id)
    fecha = str(fecha)
    ip = '192.168.20.'+str(math.ceil(id/100))
    print(ip)
    horas = requests.get(base+func+'&dato='+dato+'&fecha='+fecha, headers={'X-Forwarded-For': ip}).json()
    respuesta = {'ida': [], 'vuelta': [], 'tipo': horas['servicios'][0]['tipo']}
    for x in horas['servicios'][0]['ida']:
        respuesta['ida'].append(str(x)[:-2]+':'+str(x)[-2:])
    for x in horas['servicios'][0]['vuelta']:
        respuesta['vuelta'].append(str(x)[:-2]+':'+str(x)[-2:])
    return respuesta

#                 _
#   ___ __ _  ___| |__   ___
#  / __/ _` |/ __| '_ \ / _ \
# | (_| (_| | (__| | | |  __/
#  \___\__,_|\___|_| |_|\___|
# ---
# Comprobar si la petición está guardada y su fecha es reciente
# En caso contrario, hacer la petición a itranvías y almacenarla
def cache(cache, id_dato, tipo):
    # Hacer peticiones cambiando la ip de la cabecera dependiendo de la parada/línea
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

    max_age = 20    # Max age for the cache in seconds
    hora = datetime.datetime.now()
    if id_dato in cache.keys() and hora-cache[id_dato]['hora'] < datetime.timedelta(seconds=max_age):    # Comprobar si el dato está en caché y es suficientemente reciente
        return cache[id_dato]['datos']
    else:   # En caso contrario hacer la petición y almacenarla
        datos = peticion(id_dato, tipo)
        cache[id_dato] = {'datos': datos, 'hora': hora}
        return datos
