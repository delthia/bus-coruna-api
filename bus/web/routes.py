# bus.delthia.com - información en tiempo real del bus de Coruña
# Copyright (C) 2023  <Iago, delthia@delthia.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
    Rutas para la interfaz web de la aplicación en la que se pueden consultar
    los datos sobre las paradas y las líneas y otro tipo de información, como
    las tarifas, los enlaces entre líneas además de información sobre la pro-
    pia aplicación.
    Se utilizan las plantillas que están en la carpeta 'templates' que está en
    este mismo directorio y la información que sirven las funciones de la api
    a las que se llama directamente.
"""
from flask import Blueprint, redirect, render_template, request, send_file, url_for
import json
from bus.api.routes import rutas, jlineas, jrutas, jparadas
from bus.utils import buses_parada, buses_linea, encontrar_linea, encontrar_parada, geojson_linea, salidas #, geojson_buses
from bus import app

web = Blueprint('web', __name__, template_folder='templates', static_folder='static')


# Cargar las traducciones
with open(rutas['translate']) as t:
    translations = json.load(t)

# Página de inicio. Información sobre la página
@web.route("/")
@web.route("/inicio")
def inicio():
    lang = request.args.get('lang', type=str)    # Idioma de la página
    if not lang:    # Si no se especifica un idioma con el parámetro, tomar el valor por defecto
        lang = translations['default']
    elif lang not in translations['langs']: # Si el valor indicado no existe, eliminar el parámetro
        return redirect(url_for('web.inicio'))
    return render_template('inicio.html', lang=lang, t=translations[lang]['strings'])

# Mapa con todas las paradas
@web.route("/mapa")
def mapa():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('web.mapa', lang=translations['default']))
    return render_template('mapa.html', title=translations[lang]['titles'][0], lang=lang, t=translations[lang]['strings'])

# Lista con todas las paradas
@web.route("/paradas")
def paradas():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('web.paradas', lang=translations['default']))
    return render_template('paradas.html', title=translations[lang]['titles'][1], paradas=jparadas, lang=lang, t=translations[lang]['strings'])

# Lista con todas las líneas
@web.route("/lineas")
def lineas():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('web.lineas', lang=translations['default']))
    return render_template('lineas.html', title=translations[lang]['titles'][2], lineas=jlineas, lang=lang, t=translations[lang]['strings'])

# Parada. Muestra los próximos buses, sus características y un mapa
@web.route("/parada/<int:id_parada>")
def parada(id_parada):
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('web.parada', id_parada=id_parada, lang=translations['default']))
    parada = encontrar_parada(id_parada, jparadas)
    if parada == None:
        return render_template('404.html', i='priority_high', m=translations[lang]['sentences'][0], lang=lang, t=translations[lang]['strings']), 404
    buses = buses_parada(parada['id'], jlineas)
    if buses == {'error': 'No hay buses para esta parada'}:
        return render_template('404.html', i='remove_road', m=translations[lang]['sentences'][1], lang=lang, t=translations[lang]['strings'], lineas=parada['lineas'], leyenda=translations[lang]['sentences'][5]), 404
    elif buses == 429:
        return render_template('404.html', i='link_off', m=translations[lang]['sentences'][2], lang=lang, t=translations[lang]['strings']), 404
    return render_template('parada.html', title=parada['nombre'], buses=buses['buses']['lineas'], parada=parada, lang=lang, t=translations[lang]['strings'])

# Línea. Muestra las paradas y la posición de los buses en un diagrama. También
# muestra un mapa con el recorrido y las paradas, y una tabla con las horas de salida
@web.route("/linea/<int:id_linea>")
def linea(id_linea):
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('web.linea', id_linea=id_linea, lang=translations['default']))
    line = encontrar_linea(id_linea, jlineas)
    if line == None:
        return render_template('404.html', i='priority_high', m=translations[lang]['sentences'][3], lang=lang, t=translations[lang]['strings']), 404
    buses = buses_linea(line['id'])
    for linea in jrutas['lineas']:
        if linea['id'] == id_linea:
            break
    if buses == 429:
        return render_template('404.html', i='link_off', m=translations[lang]['sentences'][2], lang=lang, t=translations[lang]['strings']), 404
    elif buses['paradas'] == []:
        return render_template('linea.html', title=translations[lang]['titles'][3]+str(line['nombre']), paradas=linea, line=line, lang=lang, t=translations[lang]['strings'], asleep=True)
    # Traducción incompleta
    return render_template('linea.html', title=translations[lang]['titles'][3]+str(line['nombre']), paradas=linea, line=line, lang=lang, t=translations[lang]['strings'])

# Información sobre el funcionamiento de la página
@web.route("/codigo-fuente")
def fuente():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('web.fuente', lang=translations['default']))
    return render_template('fuente.html', title=translations[lang]['titles'][4], lang=lang, t=translations[lang]['strings'])

# Historial de cambios
@web.route("/cambios")
def cambios():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('web.fuente', lang=translations['default']))
    return render_template('changelog.html', title=translations[lang]['titles'][5], lang=lang, t=translations[lang]['strings'])

# Información sobre la página
@web.route("/acerca-de")
def acerca_de():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('web.about', lang=translations['default']))
    return render_template('about.html', title=translations[lang]['titles'][6], lang=lang, t=translations[lang]['strings'])

# Información de privacidad sobre la página
@web.route("/privacidad")
def privacy():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('web.privacy', lang=translations['default']))
    return render_template('privacy.html', title=translations[lang]['titles'][6], lang=lang, t=translations[lang]['strings'])

# Información sobre los precios de los tickets
@web.route("/tarifas")
def tarifas():
    lang = request.args.get('lang', type=str)
    if lang not in translations['langs']:
        return redirect(url_for('web.fuente', lang=translations['default']))
    return render_template('tarifas.html', title='Tarifas', lang=lang, t=translations[lang]['strings'])

# Service Worker que permite instalar la aplicación como PWA
@web.route("/sw.js")
def sw():
    return send_file('static/scripts/sw.js')

# robots.txt
@web.route("/robots.txt")
def robots():
    return send_file('static/robots.txt')

# Páginas de error
@app.errorhandler(404)
def _handle_404_error(e):
    if request.path.startswith('/api/'):
        # Si es una ruta de la API devolver un json con un mensaje genérico
        return {'error': 'La ruta solicitada no existe'}
    else:
        # Si no es de la API, renderizar la plantilla con un mensaje genérico
        return render_template('404.html', i='report', m='Página no encontrada', lang=translations['default'], t=translations[translations['default']]['strings']), 404
