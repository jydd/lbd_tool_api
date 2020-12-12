#!/bin/bash
# pipenv run gunicorn -w 4 --worker-class gevent -b 0.0.0.0:5000 run:app
pipenv run gunicorn -c gunicorn.py run:app
# pipenv run gunicorn -w 4 -b 0.0.0.0:5000 run:app
