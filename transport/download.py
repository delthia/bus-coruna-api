import json, requests, os.path
from transport.utils import encontrar_linea, encontrar_parada, lineas_parada
import osmnx as ox

# Hace una petición a la url especificada y devuelve la respuesta como JSON. En caso de que falle devuelve el código de error
def peticion(url):
    respuesta = requests.get(url)
    if respuesta.status_code != 200:
        return respuesta.status_code
    return respuesta.json()

# Descarga los datos desde iTranvias, genera los archivos y los almacena en variables
# Las rutas se especifican en el orden: osm, líneas, paradas, paradas-linea, paradas.geojson
def actualizar(rutas):
    # Eliminar los archivos
    try:
        os.remove(rutas[0])
        os.remove(rutas[1])
        os.remove(rutas[2])
        os.remove(rutas[3])
        os.remove(rutas[4])
    except:
        print("Ya no existían")
    # Generar los archivos nuevos
    datos = peticion('https://itranvias.com/queryitr_v3.php?dato=20160101T000000_gl_0_20160101T000000&func=7')['iTranvias']['actualizacion']
    osm(rutas[0])
    with open(rutas[0]) as archivo:
        o = json.load(archivo)
    json_lineas(datos, rutas[1])
    json_paradas(datos, rutas[2], o)
    with open(rutas[2]) as p:
        paradas = json.load(p)
    json_paradas_lineas(datos, rutas[3], paradas)
    geojson(datos, rutas[4], o)
    # Cargar los archivos
    with open(rutas[1]) as l:
        lineas = json.load(l)
    return lineas, paradas

# Consigue los datos de OSM a través de overpass, y los guarda en la ruta especificada en un archivo GeoJSON
def osm(directorio):
    stops = ox.geometries_from_place('A Coruña, Galicia, España', {'public_transport': 'platform', 'bus': 'yes'})
    stops = stops.loc[stops.geometry.type=='Point']
    stops.to_file(directorio, driver='GeoJSON')

# Genera un JSON con todas las líneas. (id, nombre, origen, destino, color)
def json_lineas(datos, directorio):
    with open(directorio, 'w') as archivo:
        archivo.write('{ "lineas": ')
        group = []
        for linea in datos['lineas']:
            group.append({'id': linea['id'], 'nombre': linea['lin_comer'], 'origen': linea['nombre_orig'], 'destino': linea['nombre_dest'], 'color': linea['color']})
        archivo.write(json.dumps(group))
        archivo.write('}')

# Genera un JSON con todas las paradas. (id, nombre, propiedades: [pavimento, banco, marquesina, papelera, iluminada], líneas: [id, nombre, color], coordenadas, corrdenadas de OpenStreetMap)
def json_paradas(datos, directorio, data):
    def find(referencia):
        for feature in data['features']:
            if 'ref' in feature['properties'] and feature['properties']['ref'] == str(referencia):
                break
        detalles = {}
        atencion = ['tactile_paving', 'bench', 'shelter', 'bin', 'lit']
        osmcoords = feature['geometry']['coordinates']
        for at in atencion:
            if at in feature['properties']:
                if feature['properties'][at] == 'yes':
                    detalles[at] = 'y'
                elif feature['properties'][at] == 'no':
                    detalles[at] = 'n'
            else:
                detalles[at] = 's'
        return detalles, osmcoords

    archivo = open(directorio, "w")
    archivo.write('{ "paradas": ')
    lins = []
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
    archivo.write('}')
    archivo.close()

# Genera un JSON con las paradas por las que pasa una línea
def json_paradas_lineas(datos, directorio, paradas):
    with open(directorio, 'w') as archivo:
        archivo.write('{ "lineas": ')
        group = []
        for linea in datos['lineas']:
            ida, vuelta = [], []
            for parada in linea['rutas'][0]['paradas']:
                ida.append(encontrar_parada(parada, paradas))
            for parada in linea['rutas'][1]['paradas']:
                vuelta.append(encontrar_parada(parada, paradas))
            group.append({'id': linea['id'], 'paradas': {'ida': ida, 'vuelta': vuelta}})
        archivo.write(json.dumps(group))
        archivo.write('}')

# Genera un GeoJSON con todas las paradas y un diálogo que enlaza a la parada y a las líneas que pasan por la parada
def geojson(datos, directorio, data):
    archivo = open(directorio, "w")
    archivo.write('var paradas = {"type": "FeatureCollection", "features": [')
    busstop = ''
    for parada in datos['paradas']:
        def find(referencia):
            for feature in data['features']:
                if 'ref' in feature['properties'] and feature['properties']['ref'] == str(referencia):
                    return feature['geometry']['coordinates']
        if lineas_parada(parada, datos) != None:
            if find(parada['id']) == None:
                busstop = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': '<a href="./parada/'+str(parada['id'])+'">'+parada['nombre']+'</a>'+lineas_parada(parada, datos)}, 'geometry': {'type': 'Point', 'coordinates': [parada['posx'], parada['posy']]},}
            else:
                l = lineas_parada(parada, datos)
                if l == '<br>':
                    # busstop = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': 'Nada <a href="./parada/'+str(parada['id'])+'">'+parada['nombre']+'</a>'+lineas_parada(parada, datos)}, 'geometry': {'type': 'Point', 'coordinates': find(parada['id'])},}
                    pass
                else:
                    busstop = {'type': 'Feature', 'properties': {'name': parada['nombre'], 'popupContent': '<a href="./parada/'+str(parada['id'])+'">'+parada['nombre']+'</a>'+lineas_parada(parada, datos)}, 'geometry': {'type': 'Point', 'coordinates': find(parada['id'])},}
        stop = str(busstop)+','
        archivo.write(stop)
    archivo.write(']};')
    archivo.close()
