#!/bin/bash
unzip -o ./service_icon.zip -d ./media

echo "Apply database migrations ...."
python3 manage.py migrate

echo "Compile messages ...."
python3 manage.py compilemessages -l ru

echo "Collect static ...."
python3 manage.py collectstatic --noinput

echo "Start app ...."
runuser -u runner -- uwsgi --socket=0.0.0.0:8080 --uid=runner --chdir=/opt/app/qms_server --wsgi-file=qms_server/wsgi.py --processes=4 --threads=2 --stats=127.0.0.1:9191 --static-map=/static=/opt/app/qms_server/static
