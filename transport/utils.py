import requests, json

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

# Genera una lista de las líneas que pasan por una parada. Se utiliza para generar los diálogos del mapa, por lo que también incluye el HTML para los enlaces
def lineas_parada(parada, datos):
    lins = '<br>'
    for linea in parada['enlaces']:
        lin = encontrar_linea(linea, datos)
        lins = lins+'<a href="./linea/'+str(linea)+'" class="simbolo_linea" style="background-color: #'+lin['color']+'">'+lin['lin_comer']+'</a>'
    return lins

# Recoge los datos actuales de los buses para una parada
def buses_parada(parada, directorio):
    try:
        dato = requests.get('https://itranvias.com/queryitr_v3.php?&func=0&dato='+str(parada)).json()
    except:
        return 429
    with open(directorio) as a:
        lista = json.load(a)
    if not 'lineas' in dato['buses']:
        return 1111
    for linea in range(0, len(dato['buses']['lineas'])):
        dato['buses']['lineas'][linea]['linea'] = encontrar_linea(dato['buses']['lineas'][linea]['linea'], lista)
    return dato

# Recoge los datos actuales de las posiciones de los buses en el recorrido de una línea
def buses_linea(linea):
    try:
        dato = requests.get('https://itranvias.com/queryitr_v3.php?&func=2&dato='+str(linea)).json()
    except:
        return 429
    return dato

# Recoge los datos de las posiciones de los buses de una línea y devuelve un GeoJSON con esa información
def geojson_buses(linea):
    try:
        dato = requests.get('http://itranvias.com/queryitr_v3.php?&func=99&mostrar=B&dato='+str(linea)).json()['mapas'][0]['buses']
    except:
        return 429
    b = []
    for sentido in range(0, len(dato)):
        for bus in range(0, len(dato[sentido]['buses'])):
            b.append({'type': 'Feature', 'properties': {'name': dato[sentido]['buses'][bus]['bus']}, 'geometry': {'type': 'Point', 'coordinates': [dato[sentido]['buses'][bus]['posx'], dato[sentido]['buses'][bus]['posy']]}})

    # return 'var buses = {"type": "FeatureCollection", "features":'+str(b)+'}'
    return '{"type": "FeatureCollection", "features":'+str(b)+'}'
