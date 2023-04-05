from flask import render_template, url_for, request, redirect, send_file
from transport import app
from transport.utils import buses_parada, buses_linea, encontrar_linea, encontrar_parada, geojson_buses
# from transport.download import cargar_datos, actualizar_datos
from transport.download import actualizar
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
# lins, pards = cargar_datos(static)
rutas = [static+'osm.json', static+'lineas.json', static+'paradas.json', static+'paradas-linea.json', static+'paradas.geojson.js']
lins, pards = actualizar(rutas)
 
idioma = 'gal'  # Idioma al que se redirige por defecto si no existe el parámetro 'lang' en la petición
# Traducciones de los mensajes de error y los títulos
frases = {'es': ['La parada no existe o no hay información disponible', 'Parece que en este momento no hay buses para esta parada', 'Error al conseguir los datos', 'La línea no existe', 'La línea no está activa en este momento'],
        'gal': ['A parada non existe ou non hai información dispoñible', 'Parece que neste momento non hai buses para esta parada', 'Erro ao conseguir os datos', 'A liña non existe', 'A liña non está activa neste momento'],
        'en': ['The stop doesn\'t exist or there isn\'t enough information', 'It looks like there are no buses for this stop', 'Error getting the data', 'The line does not exist', 'The line isn\'t currently active']}
titulos = {'es': ['Mapa (Paradas)', 'Paradas', 'Líneas', 'Línea ', 'Fuente del proyecto', 'Cambios recientes'],
            'gal': ['Mapa (Paradas)', 'Paradas', 'Liñas', 'Liña ', 'Fonte do proxecto', 'Cambios recentes'],
            'en': ['Map (Stops)', 'Stops', 'Lineas', 'Line ', 'Project source', 'Changelog']}


#             _
#  _ __ _   _| |_ __ _ ___
# | '__| | | | __/ _` / __|
# | |  | |_| | || (_| \__ \
# |_|   \__,_|\__\__,_|___/

# Página de inicio. Información sobre la página
@app.route("/")
@app.route("/inicio")
def inicio():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('inicio', lang=idioma))
    return render_template('/inicio.html', lang=lang)

# Mapa con todas las paradas
@app.route("/mapa")
def mapa():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('mapa', lang=idioma))
    return render_template('mapa.html', title=titulos[lang][0])

# Lista con todas las paradas
@app.route("/paradas")
def paradas():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('paradas', lang=idioma))
    return render_template('/paradas.html', title=titulos[lang][1], paradas=pards)

# Lista con todas las líneas
@app.route("/lineas")
def lineas():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('lineas', lang=idioma))
    return render_template('/lineas.html', title=titulos[lang][2], lineas=lins)

# Parada. Muestra los próximos buses, sus características y un mapa
@app.route("/parada/<int:id_parada>")
def parada(id_parada):
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('parada', id_parada=id_parada, lang=idioma))
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return render_template('404.html', i='priority_high', m=frases[lang][0]), 404
    buses = buses_parada(parada['id'],static+'lineas.json')
    if buses == 1111:
        return render_template('404.html', i='remove_road', m=frases[lang][1]), 404
    elif buses == 429:
        return render_template('404.html', i='link_off', m=frases[lang][2]), 404
    return render_template(lang+'/parada.html', title=parada['nombre'], buses=buses['buses']['lineas'], parada=parada)

# Línea. Muestra las paradas para una línea en un diagrama y la posición de los buses en el recorrido
@app.route("/linea/<int:id_linea>")
def linea(id_linea):
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('linea', id_linea=id_linea, lang=idioma))
    with open(static+'paradas-linea.json') as archivo:
        paradas = json.load(archivo)
    line = encontrar_linea(id_linea,lins)
    if line == None:
        return render_template('404.html', i='priority_high', m=frases[lang][3]), 404
    buses = buses_linea(line['id'])
    if buses == 429:
        print('a')
        return render_template('404.html', i='link_off', m=frases[lang][2]), 404
    elif buses['paradas'] == []:
        return render_template('404.html', i='clear_night', m=frases[lang][4]), 404
    for l in paradas['lineas']:
        if l['id'] == id_linea:
            break
    return render_template('/linea.html', title=titulos[lang][3]+str(line['nombre']), buses=buses['paradas'], linea=id_linea, paradas=l, line=line)

# Información sobre el funcionamiento de la página y la contribución a este
@app.route("/codigo-fuente")
def fuente():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('fuente', lang=idioma))
    return render_template('/fuente.html', title=titulos[lang][4])

# Historial de cambios
@app.route("/cambios")
def changelog():
    lang = request.args.get('lang', type=str)
    if not lang:
        return redirect(url_for('fuente', lang=idioma))
    return render_template('changelog.html', title=titulos[lang][5])

#     _    ____ ___
#    / \  |  _ \_ _|
#   / _ \ | |_) | |
#  / ___ \|  __/| |
# /_/   \_\_|  |___|
# --------------------------------
#  _     _
# | |   (_)_ __   ___  __ _ ___
# | |   | | '_ \ / _ \/ _` / __|
# | |___| | | | |  __/ (_| \__ \
# |_____|_|_| |_|\___|\__,_|___/
# Devuelve información sobre la línea que se especifica en <id_linea>. (color, destino, id, nombre, origen)
@app.route("/api/linea/<int:id_linea>")
def api_linea(id_linea):
    lin = encontrar_linea(id_linea,lins)
    if lin == None:
        return 'La línea no existe'
    return encontrar_linea(id_linea,lins)

# Devuelve un GeoJSON con las coordenadas de los buses de la línea que se especifica en <id_linea>
# Deshabilitado temporalmente
"""
@app.route("/api/linea/<int:id_linea>/buses/coords")
def coords_buses(id_linea):
    line = encontrar_linea(id_linea,lins)
    if line == None:
        return 'La línea no existe'
    buses = buses_linea(line['id'])
    if buses['paradas'] == []:
        return 'La línea no está activa en este momento'
    return geojson_buses(id_linea)
"""

# Devuelve las posiciones en el recorrido de los buses de la línea que se especifica en <id_linea>
@app.route("/api/linea/<int:id_linea>/buses")
def bus_linea(id_linea):
    line = encontrar_linea(id_linea, lins)
    if line == None:
        return 'La línea no existe'
    buses = buses_linea(line['id'])
    if buses['paradas'] == []:
        return 'La línea no está activa en este momento'
    return buses
    # return geojson_buses(id_linea)

# Igual que /api/linea, peor devuelve la lista de todas las líneas
@app.route("/api/lineas/")
def api_lineas():
    with open(static+'lineas.json') as l:
        return json.load(l)

#  ____                     _
# |  _ \ __ _ _ __ __ _  __| | __ _ ___
# | |_) / _` | '__/ _` |/ _` |/ _` / __|
# |  __/ (_| | | | (_| | (_| | (_| \__ \
# |_|   \__,_|_|  \__,_|\__,_|\__,_|___/
# Devuelve los próximos buses para la parada que se especifíca en <id_parada>, así como información de cada línea. (bus, distancia, estado, tiempo, última_parada); línea: [color, destino, id, nombre, origen]
@app.route("/api/parada/<int:id_parada>")
def api_parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return 'La parada no existe'
    buses = buses_parada(parada['id'],static+'lineas.json')
    return buses

# Devuelve información sobre la parada que se especifica en <id_parada>: [coordenadas, líneas: [color, id, nombre], coordenadas_openstreetmap, propiedades: [banco, papelera, iluminada, marquesina, pavimento]]
@app.route("/api/parada/<int:id_parada>/detalles")
def api_detalles_parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return 'La parada no existe'
    return parada

# Igual que /api/parada, pero devuelve la lista de todas las paradas
@app.route("/api/paradas/")
def api_paradas():
    with open(static+'paradas.json') as p:
        return json.load(p)

#                      _                               _
#  ___  ___ _ ____   _(_) ___ ___  __      _____  _ __| | _____ _ __
# / __|/ _ \ '__\ \ / / |/ __/ _ \ \ \ /\ / / _ \| '__| |/ / _ \ '__|
# \__ \  __/ |   \ V /| | (_|  __/  \ V  V / (_) | |  |   <  __/ |
# |___/\___|_|    \_/ |_|\___\___|   \_/\_/ \___/|_|  |_|\_\___|_|
@app.route("/sw.js")
def sw():
    return send_file('static/scripts/sw.js')

# robots.txt
@app.route("/robots.txt")
def r():
    return send_file('static/robots.txt')
