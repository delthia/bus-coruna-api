#!../venv/bin/python3
from transport import app
from transport.utils import datos_iniciales

origen = 'https://itranvias.com/queryitr_v3.php'
inicio = '?dato=20160101T000000_gl_0_20160101T000000&func=7'
static = 'transport/static/'

if __name__ == '__main__':
    datos_iniciales(origen+inicio, static)
    app.run(debug=True)