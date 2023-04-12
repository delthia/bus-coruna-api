#!venv/bin/python3
from transport import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
