FROM ubuntu:20.04


RUN apt-get update -y && \
	apt-get update --fix-missing && apt-get -y install python3.6 python3-dev libpq-dev gdal-bin && \
	apt-get -y install python3-pip && \
	apt-get update --fix-missing && apt-get -y install netcat iproute2

RUN mkdir -p /opt/app
COPY ./qms_server /opt/app/qms_server
COPY ./requirements.txt /opt/app/qms_server/requirements.txt
RUN pip3 install -r /opt/app/qms_server/requirements.txt

# customize
COPY ./docker/custom_files/settings_local.py /opt/app/qms_server/qms_server/settings_local.py

WORKDIR /opt/app/qms_server

ENV EXPOSE_PORT=8080

EXPOSE ${EXPOSE_PORT}

CMD python3 manage.py runserver ${EXPOSE_PORT}

# https://stackoverflow.com/a/42873832
# For development in docker using IDE. I need docker doesn't stop when 'manage.py runserver' stops.
ENTRYPOINT ["tail", "-f", "/dev/null"] 

# Alias python=python3
# /root/.bashrc https://askubuntu.com/a/321000

# Geting host ip from docker container
# ip -4 route show default | cut -d" " -f3

# Try to connect to host/port
# nc -zv 172.17.0.1 5432
