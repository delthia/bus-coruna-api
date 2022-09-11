import json, requests

def encontrar_linea(id, datos):
    for linea in datos['lineas']:
        if linea['id'] == id:
            return linea

def lineas_parada(parada, datos):
    lins = '<br>'
    for linea in parada['enlaces']:
        lin = encontrar_linea(linea, datos)
        lins = lins+'<a href="./linea/'+str(linea)+'" class="simbolo_linea" style="background-color: #'+lin['color']+'">'+lin['lin_comer']+'</a>'
    return lins

def crear_geojson(url, directorio):
    datos = requests.get(url).json()['iTranvias']['actualizacion']
    archivo = open(directorio, "w")
    cabeza = 'var paradas = {"type":"FeatureCollection","features":['
    pie = ']};'

    archivo.write(cabeza)
    busstop = ''
    for parada in datos['paradas']:
        busstop = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': parada['nombre']+lineas_parada(parada, datos)}, 'geometry': {'type': 'Point', 'coordinates': [parada['posx'], parada['posy']]},}
        stop = str(busstop)+','
        archivo.write(stop)

    archivo.write(pie)
    archivo.close()

def json_paradas(url, directorio):
    datos = requests.get(url).json()['iTranvias']['actualizacion']
    archivo = open(directorio, "w")
    cabeza = '{ "paradas": '
    pie = '}'
    lins = []
    archivo.write(cabeza)
    print(len(datos['paradas']))
    group = []
    for parada in datos['paradas']:
        single = {}
        single.clear()
        lins = []
        for enlace in parada['enlaces']:
            lin = encontrar_linea(enlace, datos)
            lins.append({"id": lin['id'], "nombre": lin['lin_comer'], "color": lin['color']})
        single = {'id': parada['id'], 'nombre': parada['nombre'], 'lineas': lins}
        group.append(single)
    archivo.write(json.dumps(group))
    archivo.write(pie)
    archivo.close()

def json_lineas(url, directorio):
    datos = requests.get(url).json()['iTranvias']['actualizacion']
    archivo = open(directorio, "w")
    cabeza = '{ "lineas": '
    pie = '}'
    archivo.write(cabeza)
    group = []
    for linea in datos['lineas']:
        single = {'id': linea['id'], 'nombre': linea['lin_comer'], 'origen': linea['nombre_orig'], 'destino': linea['nombre_dest'], 'color': linea['color']}
        group.append(single)
    archivo.write(json.dumps(group))
    archivo.write(pie)
    archivo.close()

def buses_parada(parada):
    dato = requests.get('https://itranvias.com/queryitr_v3.php?&func=0&dato='+str(parada)).json()
    with open('transport/static/lineas.json') as archivo:
        lista = json.load(archivo)
    for linea in range(0, len(dato['buses']['lineas'])):
        dato['buses']['lineas'][linea]['linea'] = encontrar_linea(dato['buses']['lineas'][linea]['linea'], lista)
    return dato

def buses_linea(linea):
    dato = requests.get('https://itranvias.com/queryitr_v3.php?&func=2&dato='+str(linea)).json()
    return dato

def encontrar_parada(id, datos):
    for parada in datos['paradas']:
        if parada['id'] == id:
            return parada