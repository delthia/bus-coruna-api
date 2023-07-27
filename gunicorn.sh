#!/bin/sh
gunicorn --chdir bus bus:app -w 2 --threads 2 -b 0.0.0.0:80
