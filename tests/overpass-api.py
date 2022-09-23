import overpass
api = overpass.API()
response = api.get('node["name"="Autoridade Portuaria"]')
response = api.get('node["name"="Avenida do Ferrocarril, 81"]')
print(response)
print('................................')
try:
    if response['features'][0]['properties']['bench'] == 'yes':
        print("Tiene banco")
    else:
        print("No tiene banco")
except:
    print("No sé si tiene banco")
try:
    if response['features'][0]['properties']['bin'] == 'yes':
        print("Tiene papelera")
except:
    print("No sé si tiene papelera")
try:
    if response['features'][0]['properties']['lit'] == 'yes':
        print("Está iluminada")
except:
    print("No sé si está iluminada")
try:
    if response['features'][0]['properties']['shelter'] == 'yes':
        print("Tiene narquesina")
except:
    print("No sé si tiene marquesina")
try:
    if response['features'][0]['properties']['tactile_paving'] == 'yes':
        print("Tiene pavimento táctil")
except:
    print("No sé si tiene pavimento táctil")
try:
    if response['features'][0]['properties']['wheelchair'] == 'yes':
        print("Es accesible para gente en silla de ruedas")
except:
    print("No sé si es accesible en silla de ruedas")