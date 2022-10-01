from flask import render_template, url_for
from transport import app
from transport.utils import buses_parada, buses_linea, encontrar_linea, encontrar_parada, datos_iniciales
import json, os

# ¡IMPORTANTE!: Cambiar a falso para que funcione en el servidor de producción
dev = True

if dev == True:
    static = 'transport/static/'
else:
    static = 'static/'
origen = 'https://itranvias.com/queryitr_v3.php'
inicio = '?dato=20160101T000000_gl_0_20160101T000000&func=7'
lins, pards = datos_iniciales(origen+inicio, static)

@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template('inicio.html')

@app.route("/mapa")
def mapa():
    # ruta = 'transport/static/paradas.geojson.js'
    return render_template('mapa.html', title='Coruña; Buses')

@app.route("/paradas")
def paradas():
    return render_template('paradas.html', title='Paradas', paradas=pards)

@app.route("/lineas")
def lineas():
    return render_template('lineas.html', title='Líneas', lineas=lins)

@app.route("/parada/<int:id_parada>")
def parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    buses = buses_parada(parada['id'],static+'lineas.json')
    # print(buses['buses']['lineas'])
    return render_template('parada.html', title='Parada', buses=buses['buses']['lineas'], parada=parada)

@app.route("/linea/<int:id_linea>")
def linea(id_linea):
    """
    with open('transport/static/lineas.json') as archivo:
        lista = json.load(archivo)
    try:
        return buses_linea(encontrar_linea(id_linea,lista)['id'])
    except:
        return 'línea no encontrada'
    """
    buses = buses_linea(encontrar_linea(id_linea,lins)['id'])
    return render_template('linea.html', title='Línea', buses=buses['paradas'])

# Temporal
@app.route("/codigo-fuente")
def fuente():
    return render_template('fuente.html', title='Fuente del proyecto')
