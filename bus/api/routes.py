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
    Rutas para la API que sirve los datos sobre el servicio de buses,
    particularmente la información sobre las paradas, y las líneas, que se
    actualiza al arrancar el programa y periódicamente, y la información en
    tiempo real sobre la posición de los buses.
"""
from flask import Blueprint
from bus.download import actualizar
from bus.utils import encontrar_linea, buses_linea, geojson_linea, salidas, encontrar_parada, buses_parada

api = Blueprint('api', __name__, url_prefix='/api')

# Configuración
dev = True

if dev == True:
    b = 'bus/'
else:
    b = ''
rutas = {
    'osm': b+'datos/osm.json',
    'translate': b+'datos/translate.json',
    'paradas': b+'datos/paradas.json',
    'lineas': b+'datos/lineas.json',
    'geojson': b+'static/paradas.geojson.js',
    'rutas': b+'datos/rutas.json',
    'queryitr': b+'datos/queryitr_v3.json'
}

# Actualizar los datos
url = 'https://itranvias.com/queryitr_v3.php?func=7&dato=20160101T000000_gl_0_20160101T000000'
jlineas, jparadas, jrutas = actualizar(url, rutas)

"""
    Información sobre las líneas
"""
# Igual que /api/linea, pero devuelve la lista de todas las líneas
@api.route("/lineas")
def lineas():
    return jlineas

# Información sobre la línea que se especifica en <id_linea>:
#    color, destino, id, nombre, origen
@api.route("/linea/<int:id_linea>")
def linea(id_linea):
    l = encontrar_linea(id_linea, jlineas)
    if l == None:
        return {'error': 'La línea no existe'}
    return l

# Posiciones en el recorrido de la línea que se especifica en <id_linea>
@api.route("/linea/<int:id_linea>/buses")
def bus_linea(id_linea):
    l = encontrar_linea(id_linea, jlineas)
    if l == None:
        return {'error': 'La línea no existe'}
    buses = buses_linea(id_linea)
    if buses == 429:
        return {'error': 'Imposible conseguir los datos'}
    elif buses['paradas'] == []:
        return {'estado': 'Línea inactiva'}
    return buses

# GeoJSON con las paradas de una línea
@api.route("/linea/<int:id_linea>/paradas")
def paradas_linea(id_linea):
    l = encontrar_linea(id_linea, jlineas)
    if l == None:
        return {'error': 'La línea no existe'}
    geojson = geojson_linea(id_linea, jrutas)
    return geojson

# Salidas de una línea
@api.route("/linea/<int:id_linea>/salidas/<int:fecha>")
def salidas_linea(id_linea, fecha):
    l = encontrar_linea(id_linea, jlineas)
    if l == None:
        return {'error': 'La línea no existe'}
    s = salidas(id_linea, fecha)
    if s == 429:
        return {'error': 'Imposible conseguir los datos'}
    return s

"""
    Información sobre las paradas
"""
# Igual que /api/parada, pero devuelve una lista con todas las paradas
@api.route("/paradas")
def paradas():
    return jparadas

# Información sobre la parada que se especifica en <id_parada>:
# [coordenadas, lineas: [color, id, nombre], coordenadas_openstreetmap,
# propiedades: [banco, papelera, iluminada, marquesina, pavimento]]
@api.route("/parada/<int:id_parada>")
def detalles_parada(id_parada):
    parada = encontrar_parada(id_parada, jparadas)
    if parada == None:
        return {'error': 'La parada no existe'}
    return parada

# Próximos buses para la parada que se especifica en <id_parada>
# También incluye información sobre cada línea:
# bus, distancia, estado, tiempo, última_parada;
# línea: [color, destino, id, nombre, origen]
@api.route("/parada/<int:id_parada>/buses")
def parada_buses(id_parada):
    parada = encontrar_parada(id_parada, jparadas)
    if parada == None:
        return {'error': 'La parada no existe'}
    buses = buses_parada(id_parada, jlineas)
    if buses == 429:
        return {'error': 'Imposible conseguir los datos'}
    return buses
