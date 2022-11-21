import json, requests, os.path

def datos_iniciales(url, dir):
    done = False
    while not done:
        if not os.path.exists(dir+'lineas.json'):
            json_lineas(url, dir+'lineas.json')
        elif not os.path.exists(dir+'paradas.geojson.js'):
            crear_geojson(url, dir+'paradas.geojson.js', dir+'paradas-osm.json')
        elif not os.path.exists(dir+'paradas.json'):
            json_paradas(url, dir+'paradas.json', dir+'paradas-osm.json')
        elif not os.path.exists(dir+'paradas-linea.json'):
            with open(dir+'paradas.json') as archivo:
                paradas = json.load(archivo)
            json_paradas_lineas(url, dir+'paradas-linea.json', paradas)
        else:
            done = True
    with open(dir+'lineas.json') as archivo:
        lineas = json.load(archivo)
    with open(dir+'paradas.json') as archivo:
        paradas = json.load(archivo)
    return lineas, paradas

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

def crear_geojson(url, directorio, osmjson):
    datos = requests.get(url).json()['iTranvias']['actualizacion']
    archivo = open(directorio, "w")
    cabeza = 'var paradas = {"type":"FeatureCollection","features":['
    pie = ']};'

    archivo.write(cabeza)
    busstop = ''
    for parada in datos['paradas']:
        def find(referencia):
            with open(osmjson) as arch:
                data = json.load(arch)
            for feature in data['features']:
                if 'ref' in feature['properties'] and feature['properties']['ref'] == str(referencia):
                    return feature['geometry']['coordinates']
        if lineas_parada(parada, datos) != None:
            if find(parada['id']) == None:
                busstop = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': '<a href="./parada/'+str(parada['id'])+'">'+parada['nombre']+'</a>'+lineas_parada(parada, datos)}, 'geometry': {'type': 'Point', 'coordinates': [parada['posx'], parada['posy']]},}
            else:
                busstop = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': '<a href="./parada/'+str(parada['id'])+'">'+parada['nombre']+'</a>'+lineas_parada(parada, datos)}, 'geometry': {'type': 'Point', 'coordinates': find(parada['id'])},}
        stop = str(busstop)+','
        archivo.write(stop)

    archivo.write(pie)
    archivo.close()

def json_paradas(url, directorio, osmjson):
    def find(referencia):
        with open(osmjson) as arch:
            data = json.load(arch)
        for feature in data['features']:
            if 'ref' in feature['properties'] and feature['properties']['ref'] == str(referencia):
                break
        detalles = {}
        atencion = ['tactile_paving', 'bench', 'shelter', 'bin', 'lit']
        osmcoords = feature['geometry']['coordinates']
        for at in atencion:
            if at in feature['properties'] and feature['properties'][at] == 'yes':
                detalles[at] = 'y'
            elif at in feature['properties'] and feature['properties'][at] == 'no':
                detalles[at] = 'n'
            else:
                detalles[at] = 's'
        return detalles, osmcoords
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
        coords = [parada['posx'], parada['posy']]
        det, osmcoords = find(parada['id'])
        single = {'id': parada['id'], 'nombre': parada['nombre'], 'propiedades': det, 'lineas': lins, 'coords': coords, 'osmcoords': osmcoords}
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
        # single = {'id': linea['id'], 'nombre': linea['lin_comer'], 'origen': linea['nombre_orig'], 'destino': linea['nombre_dest'], 'color': linea['color'], 'paradas': {'ida': linea['rutas'][0]['paradas'], 'vuelta': linea['rutas'][1]['paradas']}}
        group.append(single)
    archivo.write(json.dumps(group))
    archivo.write(pie)
    archivo.close()

def buses_parada(parada, directorio):
    try:
        dato = requests.get('https://itranvias.com/queryitr_v3.php?&func=0&dato='+str(parada)).json()
    except:
        return '429'
    with open(directorio) as archivo:
        lista = json.load(archivo)
    if not 'lineas' in dato['buses']:
        return '1111'
    for linea in range(0, len(dato['buses']['lineas'])):
        dato['buses']['lineas'][linea]['linea'] = encontrar_linea(dato['buses']['lineas'][linea]['linea'], lista)
    return dato

def buses_linea(linea):
    try:
        dato = requests.get('https://itranvias.com/queryitr_v3.php?&func=2&dato='+str(linea)).json()
    except:
        return '429'
    return dato

def encontrar_parada(id, datos):
    for parada in datos['paradas']:
        if parada['id'] == id:
            return parada

def geojson_buses(linea):
    dato = requests.get('https://itranvias.com/queryitr_v3.php?&func=99&mostrar=B&dato='+str(linea)).json()['mapas'][0]['buses']
    cabeza = 'var buses = {"type":"FeatureCollection", "features":'
    b = []
    pie = '};'

    for sentido in range(0, len(dato)):
        for bus in range(0, len(dato[sentido]['buses'])):
            b.append({'type': 'Feature', 'properties': {'name': dato[sentido]['buses'][bus]['bus']}, 'geometry': {'type': 'Point', 'coordinates': [dato[sentido]['buses'][bus]['posx'], dato[sentido]['buses'][bus]['posy']]}})

    return cabeza+str(b)+pie

def json_paradas_lineas(url, directorio, paradas):
    datos = requests.get(url).json()['iTranvias']['actualizacion']
    archivo = open(directorio, "w")
    cabeza = '{ "lineas": '
    pie = '}'
    archivo.write(cabeza)
    group = []
    # {"lineas": {"id": 1000, "paradas": {"ida": [{}, {}, {}, {}], "vuelta": [{}, {}, {}, {}]}}}
    for linea in datos['lineas']:
        ida = []
        for parada in linea['rutas'][0]['paradas']:
            ida.append(encontrar_parada(parada, paradas))
        vuelta = []
        for parada in linea['rutas'][1]['paradas']:
            vuelta.append(encontrar_parada(parada, paradas))
        single = {'id': linea['id'], 'paradas': {'ida': ida, 'vuelta': vuelta}}
        group.append(single)
    archivo.write(json.dumps(group))
    archivo.write(pie)
    archivo.close()
