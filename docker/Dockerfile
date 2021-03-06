FROM ubuntu:20.04


RUN apt-get update -y && \
	apt-get update --fix-missing && apt-get -y install python3.6 python3-dev libpq-dev gdal-bin libpcre3 libpcre3-dev unzip && \
	apt-get -y install gettext && \
	apt-get -y install python3-pip && \
	apt-get update --fix-missing && apt-get -y install netcat iproute2

RUN groupadd -r runner && useradd -s /bin/bash -g runner runner
RUN groupadd -r nginx && useradd -s /bin/bash -g nginx nginx
RUN mkdir -p /opt/app
RUN mkdir -p /opt/socket
RUN mkdir -p /tmp/nginx

COPY ./qms_server /opt/app/qms_server
COPY ./requirements.txt /opt/app/qms_server/requirements.txt

RUN chown -R runner:runner /opt/app/qms_server/static
RUN chown -R runner:runner /opt/socket
RUN chown -R nginx:nginx /tmp/nginx

# customize
COPY ./docker/custom_files/settings_local.py /opt/app/qms_server/qms_server/settings_local.py
COPY ./docker/custom_files/service_icon.zip /opt/app/qms_server/service_icon.zip
RUN pip3 install -r /opt/app/qms_server/requirements.txt

# This is hack - for to avoid check_service error for wfs layers
RUN pip3 install pyproj==1.9.6

WORKDIR /opt/app/qms_server
# RUN chown -R runner:runner /opt/app/qms_server

RUN mkdir -p /opt/app/qms_server/static
# RUN chown -R runner:runner /opt/app/qms_server/static
# bugfix https://serverfault.com/a/900708
RUN mkdir -p /opt/app/qms_server/media
# RUN chown -R runner:runner /opt/app/qms_server/media

COPY ./docker/custom_files/settings_local.py /opt/app/qms_server/qms_server/settings_local.py
COPY ./docker/custom_files/start_socket.sh /opt/app/qms_server/start_socket.sh
COPY ./docker/custom_files/start_http.sh /opt/app/qms_server/start_http.sh
COPY ./docker/custom_files/start_checking.sh /opt/app/qms_server/start_checking.sh
COPY ./docker/custom_files/uwsgi_http.ini /opt/app/qms_server/uwsgi_http.ini 
COPY ./docker/custom_files/uwsgi_socket.ini  /opt/app/qms_server/uwsgi_socket.ini
COPY ./docker/custom_files/nginx  /opt/app/nginx

RUN /bin/bash -c 'chmod +x /opt/app/qms_server/start_http.sh' 

ENV EXPOSE_PORT=8080

EXPOSE ${EXPOSE_PORT}
# USER runner
# CMD python3 manage.py runserver ${EXPOSE_PORT}

# https://stackoverflow.com/a/42873832
# For development in docker using IDE. I need docker doesn't stop when 'manage.py runserver' stops.
# ENTRYPOINT ["tail", "-f", "/dev/null"] 

# Alias python=python3
# /root/.bashrc https://askubuntu.com/a/321000

# Geting host ip from docker container
# ip -4 route show default | cut -d" " -f3

# Try to connect to host/port
# nc -zv 172.17.0.1 5432
