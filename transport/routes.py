from flask import render_template, url_for, request, redirect
from transport import app
from transport.utils import buses_parada, buses_linea, encontrar_linea, encontrar_parada, datos_iniciales, geojson_buses
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
    lang = request.args.get('lang', type=str)
    if lang == 'es':
        return render_template('inicio.html')
    elif lang == 'gal':
        return render_template('gl/inicio.html')
    else:
        return redirect(url_for('inicio', lang='gal'))

@app.route("/mapa")
def mapa():
    return render_template('mapa.html', title='Coruña; Buses')

@app.route("/paradas")
def paradas():
    lang = request.args.get('lang', type=str)
    if lang == 'es':
        return render_template('paradas.html', title='Paradas', paradas=pards)
    elif lang == 'gal':
        return render_template('gl/paradas.html', title='Paradas', paradas=pards)
    else:
        return redirect(url_for('paradas', lang='gal'))

@app.route("/lineas")
def lineas():
    return render_template('lineas.html', title='Líneas', lineas=lins)

@app.route("/parada/<int:id_parada>")
def parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return 'La parada no existe o no hay información disponible', 404
    buses = buses_parada(parada['id'],static+'lineas.json')
    if buses == '1111':
        return 'Parece que en este momento no hay buses para esta parada'
    elif buses == '429':
        return 'Error al conseguir los datos'
    lang = request.args.get('lang', type=str)
    if lang == 'es':
        return render_template('parada.html', title='Parada', buses=buses['buses']['lineas'], parada=parada)
    elif lang == 'gal':
        return render_template('gl/parada.html', title='Parada', buses=buses['buses']['lineas'], parada=parada)
    else:
        return redirect(url_for('parada', id_parada=id_parada, lang='gal'))

@app.route("/linea/<int:id_linea>")
def linea(id_linea):
    with open(static+'paradas-linea.json') as archivo:
        paradas = json.load(archivo)
    line = encontrar_linea(id_linea,lins)
    if line == None:
        return 'La línea no existe', 404
    buses = buses_linea(line['id'])
    if buses['paradas'] == []:
        return 'La línea no está activa en este momento'
    if buses == '429':
        return 'Error al conseguir los datos'
    for l in paradas['lineas']:
        if l['id'] == id_linea:
            break
    return render_template('linea.html', title='Línea', buses=buses['paradas'], linea=id_linea, paradas=l, line=line)

# Temporal
@app.route("/codigo-fuente")
def fuente():
    return render_template('fuente.html', title='Fuente del proyecto')

@app.route("/cambios")
def changelog():
    return render_template('changelog.html', title='Cambios recientes')

# API
@app.route("/api/linea/<int:id_linea>")
def api_linea(id_linea):
    lin = encontrar_linea(id_linea,lins)
    if lin == None:
        return 'La línea no existe'
    return encontrar_linea(id_linea,lins)

@app.route("/api/parada/<int:id_parada>")
def api_parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return 'La parada no existe'
    buses = buses_parada(parada['id'],static+'lineas.json')
    return buses

@app.route("/api/parada/<int:id_parada>/detalles")
def api_detalles_parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return 'La parada no existe'
    return parada

@app.route("/api/linea/<int:id_linea>/buses/coords")
def coords_buses(id_linea):
    line = encontrar_linea(id_linea,lins)
    if line == None:
        return 'La línea no existe'
    buses = buses_linea(line['id'])
    if buses['paradas'] == []:
        return 'La línea no está activa en este momento'
    return geojson_buses(id_linea)

@app.route("/api/linea/<int:id_linea>/buses")
def bus_linea(id_linea):
    line = encontrar_linea(id_linea, lins)
    if line == None:
        return 'La línea no existe'
    buses = buses_linea(line['id'])
    if buses['paradas'] == []:
        return 'La línea no está activa en este momento'
    return buses