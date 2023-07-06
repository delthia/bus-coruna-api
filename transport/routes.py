from flask import render_template, url_for, request, redirect, send_file
from transport import app
from transport.utils import buses_parada, buses_linea, encontrar_linea, encontrar_parada, geojson_linea, salidas #, geojson_buses
# from transport.download import cargar_datos, actualizar_datos
from transport.download import actualizar
import json

# ¡IMPORTANTE!: Cambiar a falso para que funcione en el servidor de producción
dev = True

if dev == True:
    b = 'transport/'
else:
    b = ''
datos, static = b+'datos/', b+'static/'
origen = 'https://itranvias.com/queryitr_v3.php'
inicio = '?dato=20160101T000000_gl_0_20160101T000000&func=7'
rutas = {'base': datos, 'static': static, 'osm': 'osm.json', 'translate': 'translate.json', 'paradas': 'paradas.json', 'lineas': 'lineas.json', 'geojson': 'paradas.geojson.js', 'rutas': 'rutas.json'}  # Innecesario. Luego se sobreescribe. Por acabar de cambiar

# Cargar las traducciones
with open(datos+rutas['translate']) as t:
    translations = json.load(t)
# Actualizar los datos
lins, pards = actualizar(origen+inicio, rutas)

#             _
#  _ __ _   _| |_ __ _ ___
# | '__| | | | __/ _` / __|
# | |  | |_| | || (_| \__ \
# |_|   \__,_|\__\__,_|___/

# Página de inicio. Información sobre la página
@app.route("/")
@app.route("/inicio")
def inicio():
    lang = request.args.get('lang', type=str)   # Idioma de la página
    if not lang:    # Si no se especifica un idioma con el parámetro, tomar el valor por defecto
        lang = translations['default']
    elif lang not in translations['langs']: # Si el valor indicado no existe, eliminar el parámetro
        return redirect(url_for('inicio'))
    return render_template('inicio.html', lang=lang, t=translations[lang]['strings'])

# Mapa con todas las paradas
@app.route("/mapa")
def mapa():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('mapa', lang=translations['default']))
    return render_template('mapa.html', title=translations[lang]['titles'][0], lang=lang, t=translations[lang]['strings'])

# Lista con todas las paradas
@app.route("/paradas")
def paradas():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('paradas', lang=translations['default']))
    return render_template('paradas.html', title=translations[lang]['titles'][1], paradas=pards, lang=lang, t=translations[lang]['strings'])

# Lista con todas las líneas
@app.route("/lineas")
def lineas():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('lineas', lang=translations['default']))
    return render_template('lineas.html', title=translations[lang]['titles'][2], lineas=lins, lang=lang, t=translations[lang]['strings'])

# Parada. Muestra los próximos buses, sus características y un mapa
@app.route("/parada/<int:id_parada>")
def parada(id_parada):
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('parada', id_parada=id_parada, lang=translations['default']))
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return render_template('404.html', i='priority_high', m=translations[lang]['sentences'][0], lang=lang, t=translations[lang]['strings']), 404
    buses = buses_parada(parada['id'],datos+'lineas.json')
    if buses == 1111:
        return render_template('404.html', i='remove_road', m=translations[lang]['sentences'][1], lang=lang, t=translations[lang]['strings'], lineas=parada['lineas'], leyenda=translations[lang]['sentences'][5]), 404
    elif buses == 429:
        return render_template('404.html', i='link_off', m=translations[lang]['sentences'][2], lang=lang, t=translations[lang]['strings']), 404
    # return render_template(lang+'/parada.html', title=parada['nombre'], buses=buses['buses']['lineas'], parada=parada, lang=lang)
    return render_template('parada.html', title=parada['nombre'], buses=buses['buses']['lineas'], parada=parada, lang=lang, t=translations[lang]['strings'])
    # return render_template(lang+'/parada.html', title=parada['nombre'], buses=buses['lineas'], parada=parada, lang=lang)

# Línea. Muestra las paradas para una línea en un diagrama y la posición de los buses en el recorrido
@app.route("/linea/<int:id_linea>")
def linea(id_linea):
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('linea', id_linea=id_linea, lang=translations['default']))
    with open(datos+rutas['rutas']) as archivo:
        paradas = json.load(archivo)
    line = encontrar_linea(id_linea,lins)
    if line == None:
        return render_template('404.html', i='priority_high', m=translations[lang]['sentences'][3], lang=lang, t=translations[lang]['strings']), 404
    buses = buses_linea(line['id'])
    for l in paradas['lineas']:
        if l['id'] == id_linea:
            break
    if buses == 429:
        return render_template('404.html', i='link_off', m=translations[lang]['sentences'][2], lang=lang, t=translations[lang]['strings']), 404
    elif buses['paradas'] == []:
        # return render_template('404.html', i='clear_night', m=translations[lang]['sentences'][4], lang=lang, t=translations[lang]['strings']), 404
        return render_template('linea.html', title=translations[lang]['titles'][3]+str(line['nombre']), paradas=l, line=line, lang=lang, t=translations[lang]['strings'], asleep=True)
    # Traducción incompleta
    return render_template('linea.html', title=translations[lang]['titles'][3]+str(line['nombre']), paradas=l, line=line, lang=lang, t=translations[lang]['strings'])

# Información sobre el funcionamiento de la página y la contribución a este
@app.route("/codigo-fuente")
def fuente():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('fuente', lang=translations['default']))
    return render_template('fuente.html', title=translations[lang]['titles'][4], lang=lang, t=translations[lang]['strings'])

# Historial de cambios
@app.route("/cambios")
def changelog():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('fuente', lang=translations['default']))
    return render_template('changelog.html', title=translations[lang]['titles'][5], lang=lang, t=translations[lang]['strings'])

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
    with open(datos+rutas['lineas']) as l:
        return json.load(l)
    
# GeoJSON con las paradas de una línea
@app.route("/api/linea/<int:id_linea>/paradas")
def paradas_linea(id_linea):
    line = encontrar_linea(id_linea, lins)
    if line == None:
        return 'La línea no existe'
    with open(datos+rutas['rutas']) as archivo:
        paradas = json.load(archivo)
    geojson = geojson_linea(line['id'], paradas)
    return geojson

# Salidas de una línea
@app.route("/api/linea/<int:id_linea>/salidas/<int:fecha>")
def salidas_linea(id_linea, fecha):
    line = encontrar_linea(id_linea, lins)
    if line == None:
        return 'La línea no existe'
    return salidas(id_linea, fecha)

#  ____                     _
# |  _ \ __ _ _ __ __ _  __| | __ _ ___
# | |_) / _` | '__/ _` |/ _` |/ _` / __|
# |  __/ (_| | | | (_| | (_| | (_| \__ \
# |_|   \__,_|_|  \__,_|\__,_|\__,_|___/
# Devuelve los próximos buses para la parada que se especifíca en <id_parada>, así como información de cada línea. (bus, distancia, estado, tiempo, última_parada); línea: [color, destino, id, nombre, origen]
@app.route("/api/parada/<int:id_parada>/buses")
def api_parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return 'La parada no existe'
    buses = buses_parada(parada['id'],datos+'lineas.json')
    return buses

# Devuelve información sobre la parada que se especifica en <id_parada>: [coordenadas, líneas: [color, id, nombre], coordenadas_openstreetmap, propiedades: [banco, papelera, iluminada, marquesina, pavimento]]
@app.route("/api/parada/<int:id_parada>/detalles")
@app.route("/api/parada/<int:id_parada>")
def api_detalles_parada(id_parada):
    parada = encontrar_parada(id_parada, pards)
    if parada == None:
        return 'La parada no existe'
    return parada

# Igual que /api/parada, pero devuelve la lista de todas las paradas
@app.route("/api/paradas/")
def api_paradas():
    with open(datos+rutas['paradas']) as p:
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

@app.route("/acerca-de")
def about():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('about', lang=translations['default']))
    return render_template('about.html', title=translations[lang]['titles'][6], lang=lang, t=translations[lang]['strings'])

@app.route("/privacidad")
def privacy():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('privacy', lang=translations['default']))
    return render_template('privacy.html', title=translations[lang]['titles'][6], lang=lang, t=translations[lang]['strings'])
