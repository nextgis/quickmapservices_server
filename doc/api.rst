.. sectionauthor:: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.ru>


NextGIS QMS Service API documentation
======================================

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
    "geoservices_status_filter_url": "https://qms.nextgis.com/api/v1/geoservices/?cumulative_status={works|problematic|failed}",
    "geoservices_search_url": "https://qms.nextgis.com/api/v1/geoservices/?search={q}",
    "geoservices_intersects_extent_url": "https://qms.nextgis.com/api/v1/geoservices/?intersects_extent={WKT|EWKT geometry}",
    "geoservices_intersects_boundary_url": "https://qms.nextgis.com/api/v1/geoservices/?intersects_boundary={WKT|EWKT geometry}",
    "geoservices_ordering_url": "https://qms.nextgis.com/api/v1/geoservices/?ordering={name|-name|id|-id|created_at|-created_at|updated_at|-updated_at",
    "geoservices_pagination_url": "https://qms.nextgis.com/api/v1/geoservices/?limit={int}&offset={int}",
    "geoservice_detail_url": "https://qms.nextgis.com/api/v1/geoservices/{id}/",
    "geoservice_status_url": "https://qms.nextgis.com/api/v1/geoservice_status/",
    "geoservice_status_detail_url": "https://qms.nextgis.com/api/v1/geoservice_status/{id}/",
    "geoservice_status_service_filter_url": "https://qms.nextgis.com/api/v1/geoservice_status/?geoservice={id}",
    "geoservice_status_cumulative_status_filter_url": "https://qms.nextgis.com/api/v1/geoservice_status/?cumulative_status={works|problematic|failed}",
    "geoservice_status_check_at_ordering_url": "https://qms.nextgis.com/api/v1/geoservice_status/?ordering={check_at|-check_at}",
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
            "epsg": 3857,
            "icon": null,
            "submitter": "349a7b2a-3795-43f7-96f9-da0615ff23c3",
            "created_at": "2017-01-10T12:11:11.131241Z",
            "updated_at": "2018-03-10T14:57:08.274807Z",
            "cumulative_status": "works",
            "extent": "SRID=4326;POLYGON ((-123.2465499999999992 48.4077100000000016, -122.7308799999999991 48.4077100000000016, -122.7308799999999991 48.7430999999999983, -123.2465499999999992 48.7430999999999983, -123.2465499999999992 48.4077100000000016))"
        },
        {
            "id": 88,
            "guid": "6db548c3-9d5c-4ad8-abeb-13cd9466849c",
            "name": "Landsat (Gis-Lab.info)",
            "desc": null,
            "type": "tms",
            "epsg": 3857,
            "icon": null,
            "submitter": "349a7b2a-3795-43f7-96f9-da0615ff23c3",
            "created_at": "2017-04-15T13:31:31.727508Z",
            "updated_at": "2017-04-15T13:31:31.727508Z",
            "cumulative_status": "works",
            "extent": "SRID=4326;POLYGON ((-123.2465499999999992 48.4077100000000016, -122.7308799999999991 48.4077100000000016, -122.7308799999999991 48.7430999999999983, -123.2465499999999992 48.7430999999999983, -123.2465499999999992 48.4077100000000016))"

        },
        {
            "id": 89,
            "guid": "b3b58d17-df8a-44b0-9804-0a2093fed157",
            "name": "OSM Veloroad",
            "desc": null,
            "type": "tms",
            "epsg": 3857,
            "icon": null,
            "submitter": "349a7b2a-3795-43f7-96f9-da0615ff23c3",
            "created_at": "2017-01-10T11:28:36.546992Z",
            "updated_at": "2017-01-10T11:28:36.546992Z",
            "cumulative_status": "failed",
            "extent": null
        },
        {
            "id": 174,
            "guid": "48f1a563-cd12-4852-b1bf-1008e23002d0",
            "name": "Dark Matter",
            "desc": null,
            "type": "tms",
            "epsg": 3857,
            "icon": null,
            "submitter": null,
            "created_at": "2016-11-14T18:08:04.486371Z",
            "updated_at": "2016-11-14T18:08:04.486371Z",
            "cumulative_status": "problematic",
            "extent": null
        }
    ]                                                                                                   

Geo Service Details
--------------------

.. http:get:: /api/v1/geoservices/{int:id}/

**Example request**:

.. sourcecode:: http

   GET /api/v1/geoservices/465/ HTTP/1.1
   Host: qms.nextgis.com
   Accept: */*

**Example response**:
    
.. sourcecode:: json

   HTTP 200 OK
   Allow: GET, HEAD, OPTIONS
   Content-Type: application/json
   Vary: Accept

   {
        "id": 465,
        "cumulative_status": "works",
        "url": "http://maps.kosmosnimki.ru/TileService.ashx?Request=gettile&LayerName=04C9E7CE82C34172910ACDBF8F1DF49A&apikey=U96GP973UH&crs=epsg:3857&z={z}&x={x}&y={y}",
        "alt_urls": [],
        "origin_url": "http://maps.kosmosnimki.ru/TileService.ashx?Request=gettile&LayerName=04C9E7CE82C34172910ACDBF8F1DF49A&apikey=U96GP973UH&crs=epsg:3857&z={z}&x={x}&y={y}",
        "guid": "cd71471d-4899-4e95-b2e5-5c7e8dd55fce",
        "name": "Kosmosnimki.ru Satellite",
        "desc": "",
        "type": "tms",
        "epsg": 3857,
        "license_name": "",
        "license_url": "",
        "copyright_text": "",
        "copyright_url": "",
        "terms_of_use_url": "",
        "created_at": "2016-11-14T18:08:04.486371Z",
        "updated_at": "2016-11-14T18:08:04.486371Z",
        "source": null,
        "source_url": null,
        "extent": null,
        "boundary": null,
        "boundary_area": null,
        "z_min": null,
        "z_max": 19,
        "y_origin_top": true,
        "icon": 77,
        "submitter": null,
        "last_status": 442280
   }

Geo Service Icon
--------------------

.. http:get:: /api/v1/icons/{int:id}/content

**Example request**:

.. sourcecode:: http

   GET /api/v1/icons/77/content HTTP/1.1
   Host: qms.nextgis.com
   Accept: */*

In response service returns icon image.
