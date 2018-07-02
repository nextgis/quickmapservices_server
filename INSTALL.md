# Установка QMS Server

## Установка необходимых пакетов  
```bash  
    sudo apt-get update
    sudo apt-get install python-virtualenv git libpq-dev python-dev gettext libjpeg-dev libtiff-dev libfreetype6-dev
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

## Структура фронтенд-части приложения
Фронтенд QMS располагается в директории ```qms_server/frontend```

Также есть общая для всех приложений nextgis.com часть, организованная в виде git сабмодуля, — ```nextgis_common```

```nextgis_common``` в свою очередь также имеет фронтенд часть - ```nextgis_common/frontend```. (Скрипты и стили ```nextgis_common``` участвуют в сборке фронтенда для конкретного приложения QMS).

## Обновление фронтенда

При необходимости внести изменения во фронтенд приложения в процессе разработки из директории ```quickmapservices_server/qms_server/``` нужно запустить сборку скриптов и стилей командой:

```bash
npm run build
``` 

На данный момент это команда и собирает итоговую сборку для продакшна, и при этом отслеживает изменения в коде.

## Используемые UI фреймворки
В проекте сосуществуют 2 UI-фреймворка — [Bootstrap Material Design](https://fezvrasta.github.io/bootstrap-material-design/) и [Vuetify](https://vuetifyjs.com/ru/). Постепенно должен быть осуществлен полный переход на Vuetify.



