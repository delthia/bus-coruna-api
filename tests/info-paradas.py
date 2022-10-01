# import overpass
# api = overpass.API()
# response = api.get('area[name = "A Coruña"][place = "municipality"];node["public_transport"="platform"]["bus"="yes"](area);')
# data = response['features']
# for i in range(0, len(data)):
#     print(data[i]['properties'])

# tactile_paving
# bench
# shelter
# bin
# lit
# ref = id
import json

with open('samples/paradas-osm.json') as archivo:
    data = json.load(archivo)

# def find(referencia):
#     for prop in data:
        # if prop['properties']['ref'] == referencia:
        #     return prop
#         print(prop['properties']['ref'])

# print(find(119))
# print(data['features'][0]['properties']['ref'])
def find(referencia):
    for feature in data['features']:
        if 'ref' in feature['properties'] and feature['properties']['ref'] == str(referencia):
                return feature['properties']

parada = find(279)
detalles = {}
atencion = ['tactile_paving', 'bench', 'shelter', 'bin', 'lit']
for at in atencion:
    if at in parada and parada[at] == 'yes':
        detalles[at] = 'y'
    elif at in parada and parada[at] == 'no':
        detalles[at] = 'n'
    else:
        detalles[at] = 's'
print(detalles)
# print(data[0]['properties']['ref'])