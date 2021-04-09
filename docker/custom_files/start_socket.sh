#!/bin/bash
unzip -o ./service_icon.zip -d ./media

echo "Make database migrations ...."
python3 manage.py makemigrations

echo "Apply database migrations ...."
python3 manage.py migrate

echo "Compile messages ...."
python3 manage.py compilemessages -l ru

echo "Collect static ...."
python3 manage.py collectstatic --noinput

echo "Start app ...."
runuser -u runner -- uwsgi --ini uwsgi_socket.ini

