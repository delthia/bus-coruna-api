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
    if parada == None:
        return 'La parada no existe o no hay información disponible'
    else:
        buses = buses_parada(parada['id'],static+'lineas.json')
        return render_template('parada.html', title='Parada', buses=buses['buses']['lineas'], parada=parada)

@app.route("/linea/<int:id_linea>")
def linea(id_linea):
    line = encontrar_linea(id_linea,lins)
    if line == None:
        return 'La línea no existe'
    else:
        buses = buses_linea(line['id'])
        if buses['paradas'] == []:
            return 'La línea no está activa en este momento'
        else:
            return render_template('linea.html', title='Línea', buses=buses['paradas'])

# Temporal
@app.route("/codigo-fuente")
def fuente():
    return render_template('fuente.html', title='Fuente del proyecto')

# API
@app.route("/api/linea/<int:id_linea>")
def api_linea(id_linea):
    lin = encontrar_linea(id_linea,lins)
    if lin == None:
        return 'La línea no existe'
    else:
        return encontrar_linea(id_linea,lins)

@app.route("/api/parada/<int:id_parada>")
def api_parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return 'La parada no existe'
    else:
        buses = buses_parada(parada['id'],static+'lineas.json')
        return buses

@app.route("/api/parada/<int:id_parada>/detalles")
def api_detalles_parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return 'La parada no existe'
    else:
        return parada