# Dockerfile

FROM ubuntu:20.04
ENV EXPOSE_PORT=8080
RUN apt-get update
RUN mkdir -p /opt/app

COPY qms.docker/quickmapservices_server /opt/app/quickmapservices_server

RUN apt-get update --fix-missing && apt-get -y install python3.6 python3-dev libpq-dev gdal-bin
RUN apt-get -y install python3-pip


RUN apt-get update --fix-missing && apt-get -y install netcat iproute2

WORKDIR /opt/app/quickmapservices_server
RUN pip3 install -r requirements.txt
WORKDIR /opt/app/quickmapservices_server/qms_server
CMD python3 manage.py runserver ${EXPOSE_PORT}

# https://stackoverflow.com/a/42873832
# For development in docker using IDE. 
# We need docker doesn't stop when 'manage.py runserver' stops.
# ENTRYPOINT ["tail", "-f", "/dev/null"] 

EXPOSE ${EXPOSE_PORT}



# /root/.bashrc https://askubuntu.com/a/321000
# get host ip from docker container
# ip -4 route show default | cut -d" " -f3
# try to connect to host/port
# nc -zv 172.17.0.1 5432

