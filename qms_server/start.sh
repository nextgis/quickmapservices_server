#!/bin/bash
unzip ./service_icon.zip -d ./media
python3 manage.py migrate
uwsgi --ini uwsgi.ini
