# Установка QMS Server

## Установка необходимых пакетов  
```bash  
    sudo apt-get update
    sudo apt-get install python-virtualenv git libpq-dev python-dev gettext
```



## Создание БД и пользователя
На сервере СУБД создаем пользователя ```qms_server``` без прав суперпользователя и без прав на создание БД.  
После создаем новую БД с названием ```qms_server```, владелец - ранее созданный пользователь ```qms_server```.   


## Установка приложения

1. Создать директории для развертывания:   
```bash  
    sudo mkdir /opt/qms_server  
    cd /opt/qms_server  
```

2. Создать виртуальное окружение:
```bash
    sudo virtualenv --no-site-packages ./env
```
  
3. Получить код:  
```bash
    sudo git clone https://github.com/nextgis/quickmapservices_server.git  
```
  
4. Установить зависимости:  
```bash
    sudo ./env/bin/pip install -r ./quickmapservices_server/requirements.txt  
```  
    
## Настройка и конфигурирование приложения

1. Скопировать конфиг продакшена из темплейта:
```bash
    sudo ./quickmapservices_server/qms_server/qms_server/settings_local.py_template ./quickmapservices_server/qms_server/qms_server/settings_local.py
```  
  
2. Открыть файл и отредактировать все записи с пометкой ```SET THIS!```. Текущие настройки можно посмотреть в корпе.
```bash
    sudo mcedit ./quickmapservices_server/qms_server/qms_server/settings_local.py
```  


3. Собрать статические файлы:
```bash
    sudo ./env/bin/python ./quickmapservices_server/qms_server/manage.py collectstatic
```  

4. Собрать файлы переводов:
```bash
    sudo ./env/bin/python ./quickmapservices_server/qms_server/manage.py compilemessages
```  

5. Инициализировать БД:
```bash
    sudo ./env/bin/python ./quickmapservices_server/qms_server/manage.py migrate
```  

6. Создать суперпользователя:
```bash
    sudo ./env/bin/python ./quickmapservices_server/qms_server/manage.py createsuperuser
```  

  
## Настройка и запуск uwsgi
  
1. Установить нужные пакеты:
```bash
    sudo apt-get install uwsgi uwsgi-plugin-python
```  

2. Создать ссылку на конфигурационный файл
```bash
    sudo ln -s /opt/qms_server/quickmapservices_server/configs/qms_server_uwsgi.ini /etc/uwsgi/apps-enabled/
```  

3. Запустить uwsgi
```bash
    sudo service uwsgi start
```  

  
## Настройка и запуск nginx
  
1. Установить нужные пакеты:
```bash
    sudo apt-get install nginx
```  

2. Создать ссылку на конфигурационный файл
```bash
    sudo ln -s /opt/qms_server/quickmapservices_server/configs/qms_server_nginx.conf /etc/nginx/sites-enabled/
```  

3. Запустить nginx
```bash
    sudo service nginx start
```  
