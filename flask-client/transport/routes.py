from flask import render_template, url_for
from transport import app
from transport.utils import crear_geojson, json_paradas, json_lineas, buses_parada, buses_linea, encontrar_linea, encontrar_parada
import os.path, json

@app.route("/")
@app.route("/inicio")
def inicio():
    return render_template('inicio.html')

@app.route("/mapa")
def mapa():
    ruta = 'transport/static/paradas.geojson.js'
    if not os.path.exists(ruta):
        print("No existía el geojson de las paradas")
        crear_geojson('https://itranvias.com/queryitr_v3.php?dato=20160101T000000_gl_0_20160101T000000&func=7', ruta)
    return render_template('mapa.html', title='Coruña; Buses')

@app.route("/paradas")
def paradas():
    ruta = 'transport/static/paradas.json'
    if not os.path.exists(ruta):
        print("No existía el json de las paradas")
        json_paradas('https://itranvias.com/queryitr_v3.php?dato=20160101T000000_gl_0_20160101T000000&func=7', ruta)
    with open(ruta) as archivo:
        lista = json.load(archivo)
    return render_template('paradas.html', title='Paradas', paradas=lista)

@app.route("/lineas")
def lineas():
    ruta = 'transport/static/lineas.json'
    if not os.path.exists(ruta):
        print("No existía el json de las líneas")
        json_lineas('https://itranvias.com/queryitr_v3.php?dato=20160101T000000_gl_0_20160101T000000&func=7', ruta)
    with open(ruta) as archivo:
        lista = json.load(archivo)
    return render_template('lineas.html', title='Líneas', lineas=lista)

@app.route("/parada/<int:id_parada>")
def parada(id_parada):
    with open('transport/static/paradas.json') as archivo:
        lista = json.load(archivo)
    # try:
    buses = buses_parada(encontrar_parada(id_parada,lista)['id'])
    return render_template('parada.html', title='Parada', buses=buses['buses']['lineas'])
    #except:
    #return 'parada no encontrada'

@app.route("/linea/<int:id_linea>")
def linea(id_linea):
    with open('transport/static/lineas.json') as archivo:
        lista = json.load(archivo)
    try:
        return buses_linea(encontrar_linea(id_linea,lista)['id'])
    except:
        return 'línea no encontrada'
