#!../venv/bin/python3
import argparse
import osmnx as ox
from transport.utils import encontrar_linea

def lineas(u, d):
    datos = requests.get(u).json()['iTranvias']['actualizacion']
    achivo = open(d, "w")
    cabeza = '{ "lineas": '
    pie = '}'
    archivo.write(cabeza)
    group = []
    for linea in datos['lineas']
        single = {'id': linea['id'], 'nombre': linea['lin_comer'], 'origen': linea['nombre_orig'], 'destino': linea['nombre_dest'], 'color': linea['color']}
        group.append(single)
    archivo.write(json.dumps(group))
    archivo.write(pie)
    archivo.close()

def paradas(u, d):
    place_name = "A Coruña, Galicia, España"
    area = ox.geocode_to_gdf(place_name)
    tags = {'public_transport': 'platform', 'bus': 'yes'}
    stops = ox.geometries_from_place(place_name, tags)
    stops.to_file('paradas-osm.geojson', driver='GeoJSON')

    def find(ref):
        with open('paradas-osm.geojson') as arch:
            data = json.load(arch)
        for freature in data['features']:
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
        return detalles, osmcoords

    datos = requests.get(u).json()['iTranvias']['actualizacion']
    archivo = open(d, "w")
    cabeza = '{ "paradas": '
    pie = '}'
    lins = []
    archivo.write(cabeza)
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

def geojson(u, d):
    datos = requests.get(u).json()['iTranvias']['actualizacion']
    archivo = open(d, "w")
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


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--lineas", help="Actualizar las líneas", action="store_true")
parser.add_argument("-p", "--paradas", help="Actualizar las paradas", action="store_true")
parser.add_argument("-g", "--geojson", help="Acutalizar el mapa", action="store_true")
parser.add_argument("-d", help="Directorio de salida", type=str)
parser.add_argument("-u", help="URL de los datos")
args = parser.parse_args()

if args.u:
    url = args.u
else:
    url = 'https://itranvias.com/queryitr_v3.php'

if args.d:
    directorio = args.d
else:
    directorio = 'static/'

if args.lineas:
    lineas(url, directorio+'lineas.json')
if args.paradas:
    paradas(url, directorio+'paradas.json')
if args.geojson:
    geojson(url, directorio+'paradas.geosjon.js')