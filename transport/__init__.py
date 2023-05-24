from flask_minify import Minify
from flask import Flask

app = Flask(__name__)
Minify(app=app, html=True, js=True, cssless=True, bypass=['paradas'])

from transport import routes
