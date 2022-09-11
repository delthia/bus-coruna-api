#!venv/bin/python3
import json, requests

r = requests.get('https://itranvias.com/queryitr_v3.php?dato=20160101T000000_gl_0_20160101T000000&func=7')
data = r.json()['iTranvias']['actualizacion']
datos = open("paradas.geojson", "w")
cabeza = 'var paradas = {"type":"FeatureCollection","features":['
pie = ']};'

def encontrar_linea(id):
    for linea in data['lineas']:
        if linea['id'] == id:
            return linea

def lineas_parada(parada):
    lins = '<br>'
    for linea in parada['enlaces']:
        lin = encontrar_linea(linea)
        lins = lins+'<span class="simbolo_linea" style="background-color: #'+lin['color']+'">'+lin['lin_comer']+'</span>'
    return lins



datos.write(cabeza)
for parada in data['paradas']:
    busstop = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': parada['nombre']+lineas_parada(parada)}, 'geometry': {'type': 'Point', 'coordinates': [parada['posx'], parada['posy']]},}
    stop = str(busstop)+','
    datos.write(stop)

datos.write(pie)
datos.close()