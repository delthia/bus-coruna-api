#!venv/bin/python3
import json
f = open('sample.json')

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