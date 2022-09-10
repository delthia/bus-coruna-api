#!venv/bin/python3
import json, requests

r = requests.get('https://itranvias.com/queryitr_v3.php?dato=20160101T000000_gl_0_20160101T000000&func=7')
data = r.json()['iTranvias']['actualizacion']
# f = open('sample.json')

# data = json.load(f)['iTranvias']['actualizacion']
direcciones = ['ida', 'vuelta']
op1 = ["1", "Línea", "Líneas"]
op2 = ["2", "Parada", "Paradas"]
ops = op1+op2


def encontrar(origen, consulta, campo):
    for x in origen:
        if x[campo] == consulta:
            return x

def parada(id):
    return encontrar(data['paradas'], id, 'id')

def linea(nombre):
    return encontrar(data['lineas'], nombre, 'lin_comer')

"""
print(parada(581))
lin = linea('5')
print('Línea '+lin['lin_comer']+'\nOrigen: '+lin['nombre_orig']+'\nDestino: '+lin['nombre_dest'])

for ruta in range(0, 2):
    print(direcciones[ruta])
    for par in lin['rutas'][ruta]['paradas']:
        print(par,'-',parada(par)['nombre'])
    if ruta < 1: print('---')
"""

tipo = input("¿Qué buscas? (Teclea el número o la primera palabra)\n1. Línea de bus\n2. Parada de bus\n> ")
while tipo not in ops:
    print("Respuesta no entre las permitidas")
    tipo = input("¿Qué buscas? (Teclea el número o la primera palabra)\n1. Línea de bus\n2. Parada de bus\n> ")
if tipo in op1:
    print("Línea de bus")
    num_linea = input("¿De qué línea quieres obtener información? Introduce su número:\n> ")
    print(linea(num_linea))
elif tipo in op2:
    print("Paradas de bus")
else:
    print("No sé como alguien se pudo saltar la comprobación")


# f.close()