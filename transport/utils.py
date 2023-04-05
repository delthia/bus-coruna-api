import requests, json, math, datetime

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
