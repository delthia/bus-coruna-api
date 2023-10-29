<p align="center">
    <picture>
        <img src="https://raw.githubusercontent.com/delthia/bus-coruna-api/main/bus/static/commute-w.svg" width="150">
    </picture>
    <br>
    <strong>bus.delthia.com - información en tiempo real del bus de Coruña</strong>
    <br>
    <br>
    <img src="https://img.shields.io/github/license/delthia/bus-coruna-api"> <img src="https://img.shields.io/github/repo-size/delthia/bus-coruna-api"> <img src="https://img.shields.io/github/v/tag/delthia/bus-coruna-api">
    <hr>
</p>

![Captura de pantalla de la página de inicio](bus/static/img/homepage.webp)

Este proyecto consiste en una página que muestra datos en tiempo real del [Bus de Coruña](https://tranviascoruna.com), combinados con información sobre las paradas y mapas con datos de [OpenStreetMap](https://osm.org).

Es una página hecha con [Flask](https://flask.palletsprojects.com) que descarga los datos de los buses, los transforma para trabajar con ellos, y sirve una página en la que se pueden consultar los datos en tiempo real, actualizados a través de una API generada por el mismo servidor. Además, inlcuye información de otras fuentes, como información sobre las paradas, a partir de [OpenStreetMap](https://osm.org).

Aunque incluye elementos con JavaScript, como los mapas o la habilidad de actualizar los datos en tiempo real, es posible consultar las paradas y sus datos sin javascript.

## PWA: Aplicación Web Progresiva
![página de inicio en android](bus/static/img/readme-screenshots/inicio.webp)
![página de inicio en android](bus/static/img/readme-screenshots/mapa.webp)
![página de inicio en android](bus/static/img/readme-screenshots/paradas.webp)
![página de inicio en android](bus/static/img/readme-screenshots/parada.webp)
![página de inicio en android](bus/static/img/readme-screenshots/lineas.webp)
![página de inicio en android](bus/static/img/readme-screenshots/linea.webp)

La página se puede como una Aplicación Web Progresiva, por lo que se puede instalar en un télefono como una aplicación nativa, almacenando algunos recursos y creando un lanzador con atajos (solo funcionan en Chrome).

Se puede instalar desde cualquier navegador web, pero para tener todas las funcionalidades, recomiendo utilizar Chrome. Los atajos del lanzador no funcionan en Firefox.

## Origen de los datos
Esta página contiene datos públicos de varias fuentes. La mayoría de los datos provienen de la página de la Compañía de Tranvías ([itranvias.com](https://itranvias.com)), de donde se obtiene una lista de paradas, líneas y relaciones entre estas. Estos datos se transforman en un JSON que los relaciona entre sí y los une con la información geográfica de [OpenStreetMap](https://osm.org), de donde se obtienen las características de la parada y una ubicación más precisa con respecto al mapa que se utiliza.

Los recorridos de las líneas que se muestran en un mapa en la página de cada línea se descargan de [esta página del Ministerio de Transportes, Movilidad y Agenda Urbana](https://nap.mitma.es/Files/Detail/1376).

Aunque se modifica la estructura de los datos para almacenarlos, la información no se modifica, y se muestra tal y como se obtiene de las fuentes.

## Licencia
Este repositorio está bajo la licencia [AGPL-v3](https://www.gnu.org/licenses/agpl-3.0.html), de modo que es software libre.

### Licencias de los datos

| Fuente | Licencia |
|--------|----------|
| [NAP (mitma)](https://nap.mitma.es/) | [Consultar aquí](https://nap.mitma.es/licencia-datos) |
| [OpenStreetMap](https://openstreetmap.org) |  [ODbL](https://opendatacommons.org/licenses/odbl/) |
| [iTranvias](https://itranvias.com) | - |

### Módulos que se utilizan

| Nombre | Licencia |
|--------|----------|
| [Flask](https://flask.palletsprojects.com/) | [BSD-3-Clause License](https://flask.palletsprojects.com/en/3.0.x/license/) |
| [Gunicorn](https://gunicorn.org) | [MIT License](https://github.com/benoitc/gunicorn/blob/master/LICENSE) |
| [Flask-minify](https://github.com/mrf345/flask_minify/) | [MIT License](https://github.com/mrf345/flask_minify/blob/master/LICENSE) |
| [Flask-caching](https://github.com/pallets-eco/flask-caching) | [BSD-3-Clause License](https://github.com/pallets-eco/flask-caching/blob/master/LICENSE) |
| [requests](https://requests.readthedocs.io/en/latest/) | [Apache-2.0 License](https://github.com/psf/requests/blob/main/LICENSE) |
