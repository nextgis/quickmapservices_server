.. sectionauthor:: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.ru>


Документация NextGIS QMS Service API
=====================================

Api Root
----------

.. http:get:: /api/v1/

**Example request**:

.. sourcecode:: http

   GET /api/v1/ HTTP/1.1
   Host: qms.nextgis.com
   Accept: */*

**Example response**:
    
.. sourcecode:: json

   HTTP 200 OK
   Allow: GET, HEAD, OPTIONS
   Content-Type: application/json
   Vary: Accept

   {
    "geoservices_url": "https://qms.nextgis.com/api/v1/geoservices/",
    "geoservices_type_filter_url": "https://qms.nextgis.com/api/v1/geoservices/?type={tms|wms|wfs|geojson}",
    "geoservices_epsg_filter_url": "https://qms.nextgis.com/api/v1/geoservices/?epsg={any_epsg_code}",
    "geoservices_search_url": "https://qms.nextgis.com/api/v1/geoservices/?search={q}",
    "geoservices_ordering_url": "https://qms.nextgis.com/api/v1/geoservices/?ordering={name|-name|id|-id}",
    "geoservices_pagination_url": "https://qms.nextgis.com/api/v1/geoservices/?limit={int}&offset={int}",
    "geoservice_detail_url": "https://qms.nextgis.com/api/v1/geoservices/{id}/",
    "icons_url": "https://qms.nextgis.com/api/v1/icons/",
    "icons_search_url": "https://qms.nextgis.com/api/v1/icons/?search={q}",
    "icons_pagination_url": "https://qms.nextgis.com/api/v1/icons/?limit={int}&offset={int}",
    "icon_detail_url": "https://qms.nextgis.com/api/v1/icons/{id}/",
    "icon_content_url": "https://qms.nextgis.com/api/v1/icons/{id}/content",
    "icon_resized_content_url": "https://qms.nextgis.com/api/v1/icons/{id}/content?width={16<=x<=64}&height={16<=y<=64}",
    "default_icon_url": "https://qms.nextgis.com/api/v1/icons/default"
   }

Geo Service List
-------------------------

.. http:get:: /api/v1/geoservices/

**Example request**:

.. sourcecode:: http

   GET /api/v1/geoservices/ HTTP/1.1
   Host: qms.nextgis.com
   Accept: */*

**Example response**:
    
.. sourcecode:: json

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [
        {
            "id": 98,
            "guid": "fd15d9a6-1ff9-4af6-a60f-6e88e8a309e3",
            "name": "OSM Mapnik",
            "desc": "Моя любимая подложка!",
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 88,
            "guid": "6db548c3-9d5c-4ad8-abeb-13cd9466849c",
            "name": "Landsat (Gis-Lab.info)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 89,
            "guid": "b3b58d17-df8a-44b0-9804-0a2093fed157",
            "name": "OSM Veloroad",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 174,
            "guid": "48f1a563-cd12-4852-b1bf-1008e23002d0",
            "name": "Dark Matter",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        }
    ]                                                                                                   

Geo Service Details
--------------------

.. http:get:: /api/v1/geoservices/{int:id}/

**Example request**:

.. sourcecode:: http

   GET /api/v1/geoservices/464/ HTTP/1.1
   Host: qms.nextgis.com
   Accept: */*

**Example response**:
    
.. sourcecode:: json

   HTTP 200 OK
   Allow: GET, HEAD, OPTIONS
   Content-Type: application/json
   Vary: Accept

   {
    "id": 464,
    "guid": "dfaaff6f-61e0-4cf9-8466-1bf51dd65de2",
    "name": "2gis Map",
    "desc": null,
    "type": "tms",
    "epsg": 3857,
    "license_name": null,
    "license_url": null,
    "copyright_text": null,
    "copyright_url": null,
    "terms_of_use_url": null,
    "url": "http://tile2.maps.2gis.com/tiles?x={x}&y={y}&z={z}&v=1.1",
    "z_min": null,
    "z_max": null,
    "y_origin_top": false,
    "icon": 76
   }
