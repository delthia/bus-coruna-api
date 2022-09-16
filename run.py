#!venv/bin/python3
from transport import app
from transport.utils import datos_iniciales

if __name__ == '__main__':
    app.run(debug=True)
