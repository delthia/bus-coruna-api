#!venv/bin/python3
import json
"""
f = open('samples/sample.json')

data = json.load(f)['iTranvias']['actualizacion']

# Tarifas y sus precios
print("########################\n# Tarifas del servicio #\n########################")
for precio in data['precios']['tarifas']:
    print(precio['tarifa']) # Nombre de la tarifa
    print(str(precio['precio'])+'€') # Importe a pagar
print("\n#################\n# Observaciones #\n#################")
for observacion in data['precios']['observaciones']:
    print(observacion)

# Línea y sus paradas
print("\n##########\n# Líneas #\n##########")
for linea in data['lineas']:
    print(linea['lin_comer'],linea['id'],linea['color'],)
    for ruta in linea['rutas']:
        print(ruta['ruta'])
        for parada in ruta['paradas']:
            print(parada)

# Paradas
print("\n###########\n# Paradas #\n###########")
for parada in data['paradas']:
    print(parada['id'],parada['nombre'])
    for enlace in parada['enlaces']:
        print(enlace)

f.close()
"""

"""
archivo = open('samples/sample-parada.json')
parada = json.load(archivo)['buses']['lineas']
for linea in parada:
    print('Línea ',linea['linea'])
    for bus in linea['buses']:
        print('Bus',bus['bus'],'a',bus['distancia'],'m,',bus['tiempo'],'\'.')

archivo.close()
"""
import requests
dato = requests.get('https://itranvias.com/queryitr_v3.php?&func=0&dato=565').json()
print(len(dato['buses']['lineas']))
for linea in range(0, len(dato['buses']['lineas'])):
   dato['buses']['lineas'][linea]['linea']