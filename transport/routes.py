from flask import render_template, url_for, request, redirect, send_file
from transport import app
from transport.utils import buses_parada, buses_linea, encontrar_linea, encontrar_parada, geojson_buses
from transport.download import cargar_datos, actualizar_datos
import json, os

# ¡IMPORTANTE!: Cambiar a falso para que funcione en el servidor de producción
dev = True

if dev == True:
    static = 'transport/static/'
else:
    static = 'static/'
origen = 'https://itranvias.com/queryitr_v3.php'
inicio = '?dato=20160101T000000_gl_0_20160101T000000&func=7'
# lins, pards = datos_iniciales(origen+inicio, static)
# actualizar_datos(origen+inicio, static)
lins, pards = cargar_datos(static)

idioma = 'gal'

@app.route("/")
@app.route("/inicio")
def inicio():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('inicio', lang=idioma))
    return render_template('/inicio.html', lang=lang)

@app.route("/mapa")
def mapa():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('mapa', lang=idioma))
    return render_template('mapa.html', title='Mapa (Paradas)')

@app.route("/paradas")
def paradas():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('paradas', lang=idioma))
    return render_template('/paradas.html', title='Paradas', paradas=pards)

@app.route("/lineas")
def lineas():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('lineas', lang=idioma))
    return render_template('/lineas.html', title='Líneas', lineas=lins)

@app.route("/parada/<int:id_parada>")
def parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        # return 'La parada no existe o no hay información disponible', 404
        return render_template('404.html', i='priority_high', m='La parada no existe o no hay información disponible'), 404
    buses = buses_parada(parada['id'],static+'lineas.json')
    if buses == 1111:
        # return 'Parece que en este momento no hay buses para esta parada'
        return render_template('404.html', i='remove_road', m='Parece que en este momento no hay buses para esta parada'), 404
    elif buses == 429:
        # return 'Error al conseguir los datos'
        return render_template('404.html', i='link_off', m='Error al conseguir los datos'), 404
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('parada', id_parada=id_parada, lang=idioma))
    return render_template(lang+'/parada.html', title=parada['nombre'], buses=buses['buses']['lineas'], parada=parada)

@app.route("/linea/<int:id_linea>")
def linea(id_linea):
    with open(static+'paradas-linea.json') as archivo:
        paradas = json.load(archivo)
    line = encontrar_linea(id_linea,lins)
    if line == None:
        # return 'La línea no existe', 404
        return render_template('404.html', i='priority_high', m='La línea no existe'), 404
    buses = buses_linea(line['id'])
    if buses == 429:
        print('a')
        # return 'Error al conseguir los datos'
        return render_template('404.html', i='link_off', m='Error al conseguir los datos'), 404
    elif buses['paradas'] == []:
        # return 'La línea no está activa en este momento'
        return render_template('404.html', i='clear_night', m='La línea no está activa en este momento'), 404
    for l in paradas['lineas']:
        if l['id'] == id_linea:
            break
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('linea', id_linea=id_linea, lang=idioma))
    return render_template(lang+'/linea.html', title='Línea '+str(line['nombre']), buses=buses['paradas'], linea=id_linea, paradas=l, line=line)

# Temporal
@app.route("/codigo-fuente")
def fuente():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('fuente', lang=idioma))
    return render_template('/fuente.html', title='Fuente del proyecto')

@app.route("/cambios")
def changelog():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('fuente', lang=idioma))
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
    # return buses
    return geojson_buses(id_linea)

@app.route("/api/paradas/")
def api_paradas():
    with open(static+'paradas.json') as p:
        return json.load(p)

@app.route("/api/lineas/")
def api_lineas():
    with open(static+'lineas.json') as l:
        return json.load(l)

# service worker
@app.route("/sw.js")
def sw():
    return send_file('static/scripts/sw.js')
