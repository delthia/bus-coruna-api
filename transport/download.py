import json, requests, time
from transport.utils import encontrar_linea, encontrar_parada
# import osmnx as ox

def actualizar(url, dirs):
    r = 3   # Número de veces que se intentará hacer la petición si no funciona
    d = 30  # Retardo en segundos entre los reintentos
    for x in range(0, r):
        respuesta = requests.get(url)       # Hacer la petición
        if respuesta.status_code == 200:    # Si es correcta, guardar la respuesta en json y terminar el bucle
            respuesta = respuesta.json()['iTranvias']['actualizacion']
            break
        else:   # En caso contrario esperar y volver a intentarlo
            time.sleep(d)

    # Generar los archivos
    json_lineas(respuesta, dirs['base']+dirs['lineas'])
    # datos_osm(dirs['base']+dirs['osm'])
    with open(dirs['base']+dirs['osm']) as a:
        osm = json.load(a)
    json_paradas(respuesta, dirs['base']+dirs['paradas'], osm)
    with open(dirs['base']+dirs['paradas']) as a:
        paradas = json.load(a)
    json_rutas(respuesta, dirs['base']+dirs['rutas'], paradas)
    geojson(paradas, dirs['static']+dirs['geojson'])
    # Cargar el resto de archivos
    with open(dirs['base']+dirs['lineas']) as a:
        lineas = json.load(a)

    return lineas, paradas

# Genera un JSON con todas las líneas. (id, nombre, origen, destino, color)
def json_lineas(datos, dir):
    with open(dir, 'w') as f:
        d = {'lineas': []}
        for l in datos['lineas']:
            d['lineas'].append({'id': l['id'], 'nombre': l['lin_comer'], 'origen': l['nombre_orig'], 'destino': l['nombre_dest'], 'color': l['color']})
        f.write(json.dumps(d))

# Genera un JSON con todas las paradas. (id, nombre, propiedades: [pavimento, banco, marquesina, papelera, iluminada], líneas: [id, nombre, color], coordenadas, coordenadas de OpenStreetMap)
def json_paradas(datos, dir, osm):
    def find(ref):
        detalles = {}
        osmcoords = []
        for f in osm['features']:
            if 'ref' in f['properties'] and f['properties']['ref'] == str(ref):
                detalles = {}
                propiedades = ['tactile_paving', 'bench', 'shelter', 'bin', 'lit']  # Propiedades que se guardarán
                osmcoords = f['geometry']['coordinates'] # Coordenadas de la parada a partir de openstreetmap
                for p in propiedades:
                    if p in f['properties'] and f['properties'][p] == 'yes':
                        detalles[p] = 'y'
                    elif p in f['properties'] and f['properties'][p] == 'no':
                        detalles[p] = 'n'
                    else:
                        detalles[p] = 's'
                break
                # return detalles, osmcoords
        return detalles, osmcoords

    # Generar el archivo
    with open(dir, 'w') as a:
        o = {'paradas': []}
        for p in datos['paradas']:  # Para cada parada
            if not p['enlaces'] == []:  # Evitar las paradas que no tienen enlaces
                d, osmcoords = find(p['id'])    # Buscar los datos en la respuesta de osm
                l = []
                for e in p['enlaces']:  # Generar una lista con los detalles de las líneas que pasan por la parada. (id, nombre, color)
                    linea = encontrar_linea(e, datos)
                    l.append({'id': linea['id'], 'nombre': linea['lin_comer'], 'color': linea['color']})
                parada = {'id': p['id'], 'nombre': p['nombre'], 'propiedades': d, 'lineas': l, 'coords': [p['posx'], p['posy']], 'osmcoords': osmcoords}
                o['paradas'].append(parada)
        a.write(json.dumps(o))  # Escribir la parada al archivo

# Genera un JSON con las paradas por las que pasa cada línea
def json_rutas(datos, dir, paradas):
    with open(dir, 'w') as a:
        o = {'lineas': []}
        for l in datos['lineas']:
            linea = {'id': l['id'], 'paradas': {'ida': [], 'vuelta': []}}
            for p in l['rutas'][0]['paradas']:
                linea['paradas']['ida'].append(encontrar_parada(p, paradas))
            for p in l['rutas'][1]['paradas']:
                linea['paradas']['vuelta'].append(encontrar_parada(p, paradas))
            o['lineas'].append(linea)
        a.write(json.dumps(o))

# Genera un GeoJSON con todas las paradas y un diálogo que enlaza a la parada y a las líneas que pasan por la parada
def geojson(datos, dir):
    with open(dir, 'w') as a:
        o = {'type': 'FeatureCollection', 'features': []}
        for p in datos['paradas']:
            lineas = '<br>'
            for l in p['lineas']:
                lineas += '<a href="./linea/'+str(l['id'])+'" class="simbolo_linea" style="background-color: #'+l['color']+'">'+l['nombre']+'</a>'
            if p['osmcoords'] == []:
                o['features'].append({'type': 'Feature', 'properties': {'name': p['nombre'], 'popupContent': '<a href="./parada/'+str(p['id'])+'">'+p['nombre']+'</a>'+lineas}, 'geometry': {'type': 'Point', 'coordinates': p['coords']}})
            else:
                o['features'].append({'type': 'Feature', 'properties': {'name': p['nombre'], 'popupContent': '<a href="./parada/'+str(p['id'])+'">'+p['nombre']+'</a>'+lineas}, 'geometry': {'type': 'Point', 'coordinates': p['osmcoords']}})
        a.write('var paradas = '+json.dumps(o)+';')

# Descarga los datos de osm a través de overpass y los guarda en un archivo GeoJSON
def datos_osm(dir):
    stops = ox.geometries_from_place('A Coruña, Galicia, España', {'public_transport': 'platform', 'bus': 'yes'})
    stops = stops.loc[stops.geometry.type=='Point']
    stops.to_file(dir, driver='GeoJSON')
