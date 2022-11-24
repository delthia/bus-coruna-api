import json, requests, os.path
from os import remove
from transport.utils import encontrar_linea, encontrar_parada, lineas_parada
# import osmnx as ox

def cargar_datos(dir):
    if not os.path.exists(dir+'lineas.json') or not os.path.exists(dir+'paradas.json'):
        actualizar_datos('https://itranvias.com/queryitr_v3.php?dato=20160101T000000_gl_0_20160101T000000&func=7', dir)
    with open(dir+'lineas.json') as a:
        lineas = json.load(a)
    with open(dir+'paradas.json') as a:
        paradas = json.load(a)
    return lineas, paradas

def actualizar_datos(url, dir):
    """
    place_name = "A Coruña, Galicia, España"
    area = ox.geocode_to_gdf(place_name)

    tags = {'public_transport': 'platform', 'bus': 'yes'}
    stops = ox.geometries_from_place(place_name, tags)
    stops.to_file(dir+'osm.json', driver='GeoJSON')
    """
    # datos_osm(dir+'osm.json')
    # ox.geometries_from_place(str(ox.geocode_to_gdf("A Coruña, Galicia, España")), str({'public_transport': 'platform', 'bus': 'yes'})).to_file('osm.json', driver='GeoJSON')
    json_lineas(url, dir+'lineas.json')
    json_paradas(url, dir+'paradas.json', dir+'osm.json')
    crear_geojson(url, dir+'paradas.geojson.js', dir+'osm.json')
    with open(dir+'paradas.json') as a:
        paradas = json.load(a)
    json_paradas_lineas(url, dir+'paradas-linea.json', paradas)
    # os.remove(dir+'osm.json')

def datos_osm(d):
    p = "A Coruña, Galicia, España"
    t = {'public_transport': 'platform', 'bus': 'yes'}
    s = ox.geometries_from_place(p, t)
    s.to_file(str(d), driver='GeoJSON')

def json_lineas(url, directorio):
    try:
        datos = requests.get(url).json()['iTranvias']['actualizacion']
    except:
        return 429
    archivo = open(directorio, "w")
    archivo.write('{ "lineas": ')
    group = []
    for linea in datos['lineas']:
        single = {'id': linea['id'], 'nombre': linea['lin_comer'], 'origen': linea['nombre_orig'], 'destino': linea['nombre_dest'], 'color': linea['color']}
        group.append(single)
    archivo.write(json.dumps(group))
    archivo.write('}')
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
            if at in feature['properties']:
                if feature['properties'][at] == 'yes':
                    detalles[at] = 'y'
                elif feature['properties'][at] == 'no':
                    detalles[at] = 'n'
            else:
                detalles[at] = 's'
        return detalles, osmcoords

    try:
        datos = requests.get(url).json()['iTranvias']['actualizacion']
    except:
        return 429
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

def json_paradas_lineas(url, directorio, paradas):
    try:
        datos = requests.get(url).json()['iTranvias']['actualizacion']
    except:
        return 429
    archivo = open(directorio, "w")
    archivo.write('{ "lineas": ')
    group = []
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
    archivo.write('}')
    archivo.close()

def crear_geojson(url, directorio, osmjson):
    try:
        datos = requests.get(url).json()['iTranvias']['actualizacion']
    except:
        return 429
    archivo = open(directorio, "w")
    archivo.write('var paradas = {"type": "FeatureCollection", "features": [')
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
