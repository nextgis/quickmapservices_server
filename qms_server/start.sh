#!/bin/bash
unzip ./service_icon.zip -d ./media
python3 manage.py migrate
python3 manage.py collectstatic
uwsgi --ini uwsgi.ini
