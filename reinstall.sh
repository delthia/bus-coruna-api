#!/usr/bin/bash
# Actualizar los cambios
git reset --hard
git pull
# Desinstalar el contendor anterior y borrar su imagen
docker stop bus && docker rm bus && docker image rm delthia/buscoruna
# Cambiar a modo producción
sed -i 's/dev = True/dev = False/' bus/api/routes.py
# Crear la imagen nueva
docker build -t delthia/buscoruna .
# Crear el contenedor nuevo
docker run -t -d -p 31480:80 --restart unless-stopped --name bus delthia/buscoruna
