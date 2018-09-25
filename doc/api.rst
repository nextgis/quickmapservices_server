.. sectionauthor:: Dmitry Baryshnikov <dmitry.baryshnikov@nextgis.ru>


NextGIS QMS Service API documentation
======================================

API Root
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
    
Geo Service filtered list
--------------------------

.. http:get:: /api/v1/geoservices/?type={tms|wms|wfs|geojson}&epsg={any_epsg_code}&limit={int}&offset={int}

**Example request**:

.. sourcecode:: http

   GET /api/v1/geoservices/?type=tms&epsg=3857&limit=15&offset=0 HTTP/1.1
   Host: qms.nextgis.com
   Accept: */*

**Example response**:
    
.. sourcecode:: json

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "count": 617,
        "next": "https://qms.nextgis.com/api/v1/geoservices/?epsg=3857&limit=15&offset=15&type=tms",
        "previous": null,
        "results": [
            {
                "id": 979,
                "guid": "086150f6-ea8e-4326-a69b-8b7a19dc3f0e",
                "name": "2013 aerial imagery for San Juan County WA",
                "desc": "This service is imported from OSMLab. OSMLab id: sjcgis.org-Aerials_2013_WM. Country: United States",
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
                "id": 1157,
                "guid": "4fb9effb-a33e-4e14-9e9b-2dd138f327d4",
                "name": "2016 aerial imagery for San Juan County WA",
                "desc": "This service is imported from OSMLab. OSMLab id: sjcgis.org-Aerials_2016_WM. Country: United States",
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
                "id": 576,
                "guid": "05c3609c-1aec-4133-9097-8b09ef4691a6",
                "name": "4UMaps",
                "desc": "Tiles copyrights: 4UMaps, http://www.4umaps.eu",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": null,
                "created_at": "2016-11-14T18:08:04.486371Z",
                "updated_at": "2016-11-14T18:08:04.486371Z",
                "cumulative_status": "problematic",
                "extent": null
            },
            {
                "id": 1395,
                "guid": "add42680-4456-446c-abbb-4b7cc30ded10",
                "name": "5 stories buildings in Moscow",
                "desc": "5 stories buildings in Moscow. Experiment with TMS link from nextgis.com",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": "349a7b2a-3795-43f7-96f9-da0615ff23c3",
                "created_at": "2017-09-06T05:58:08.381078Z",
                "updated_at": "2017-09-06T05:58:08.382104Z",
                "cumulative_status": "works",
                "extent": null
            },
            {
                "id": 810,
                "guid": "012d7f79-8d97-4a2a-b4b2-819d69ef1ada",
                "name": "7th Series (OS7)",
                "desc": "This service is imported from OSMLab. OSMLab id: OS7. Country: United Kingdom",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": "349a7b2a-3795-43f7-96f9-da0615ff23c3",
                "created_at": "2017-01-10T07:18:09.939512Z",
                "updated_at": "2017-01-10T07:18:09.939512Z",
                "cumulative_status": "problematic",
                "extent": "SRID=4326;POLYGON ((-5.9260700000000002 54.8163300000000007, -2.7949700000000002 54.8163300000000007, -2.7949700000000002 56.8617500000000007, -5.9260700000000002 56.8617500000000007, -5.9260700000000002 54.8163300000000007))"
            },
            {
                "id": 917,
                "guid": "a691b422-cdfe-41b8-aac6-13e60392bd9c",
                "name": "AGIV Flanders most recent aerial imagery",
                "desc": "This service is imported from OSMLab. OSMLab id: AGIV. Country: Belgium",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": "349a7b2a-3795-43f7-96f9-da0615ff23c3",
                "created_at": "2017-01-10T10:28:08.238619Z",
                "updated_at": "2018-05-19T14:14:21.963058Z",
                "cumulative_status": "works",
                "extent": "SRID=4326;POLYGON ((2.5331800000000002 50.6820000000000022, 5.9203999999999999 50.6820000000000022, 5.9203999999999999 51.5109899999999996, 2.5331800000000002 51.5109899999999996, 2.5331800000000002 50.6820000000000022))"
            },
            {
                "id": 649,
                "guid": "7eea7b32-920c-4b13-a38d-77ad25c728db",
                "name": "AGRI black-and-white 2.5m",
                "desc": "This service is imported from OSMLab. OSMLab id: AGRI-black_and_white-2.5m",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": "7e7630e3-76c6-4e57-9116-dcfd4b72a05e",
                "created_at": "2016-12-06T15:21:07.105613Z",
                "updated_at": "2016-12-06T15:21:07.105613Z",
                "cumulative_status": "works",
                "extent": "SRID=4326;POLYGON ((112.2877799999999979 -44.0601300000000009, 156.6276100000000042 -44.0601300000000009, 156.6276100000000042 -9.9924099999999996, 112.2877799999999979 -9.9924099999999996, 112.2877799999999979 -44.0601300000000009))"
            },
            {
                "id": 575,
                "guid": "ba32909f-0b51-42f9-83e8-7bd078f77633",
                "name": "Alberding (sorbian)",
                "desc": "",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": null,
                "created_at": "2016-11-14T18:08:04.486371Z",
                "updated_at": "2016-11-14T18:08:04.486371Z",
                "cumulative_status": "failed",
                "extent": null
            },
            {
                "id": 634,
                "guid": "467325dd-bb3b-4a01-b9bf-d9dab0560d85",
                "name": "Apple iPhoto",
                "desc": "",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": "349a7b2a-3795-43f7-96f9-da0615ff23c3",
                "created_at": "2016-11-25T12:17:37.393522Z",
                "updated_at": "2016-11-25T12:17:37.393522Z",
                "cumulative_status": "problematic",
                "extent": null
            },
            {
                "id": 2336,
                "guid": "bbf3aa67-eace-4735-837e-799a95e3f0b8",
                "name": "Architecture guide by trolleway",
                "desc": "",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": "7e7630e3-76c6-4e57-9116-dcfd4b72a05e",
                "created_at": "2018-08-15T10:34:02.188501Z",
                "updated_at": "2018-08-15T10:39:14.466196Z",
                "cumulative_status": "works",
                "extent": "SRID=4326;POLYGON ((19.6008225487717525 54.5197084565585897, 60.7214426877434406 54.5197084565585897, 60.7214426877434406 60.7951778499222044, 19.6008225487717525 60.7951778499222044, 19.6008225487717525 54.5197084565585897))"
            },
            {
                "id": 1233,
                "guid": "23769bbc-8003-4d4e-8471-f5a435e48af9",
                "name": "Art Noveau architecture Riga",
                "desc": "Scan from \"Art Noveau architecture Riga\" book, 2008",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": "7e7630e3-76c6-4e57-9116-dcfd4b72a05e",
                "created_at": "2017-05-22T18:41:45.703437Z",
                "updated_at": "2017-05-22T18:41:45.703437Z",
                "cumulative_status": "works",
                "extent": null
            },
            {
                "id": 2292,
                "guid": "43513f89-1ccb-40a6-8e32-f2824c6f3113",
                "name": "ASTER Global Digital Elevation Model (GDEM) Color Shaded Relief",
                "desc": "",
                "type": "tms",
                "epsg": 3857,
                "icon": 71,
                "submitter": "4b55ea1e-7df2-4a7c-ba16-78df93931966",
                "created_at": "2018-07-11T18:02:28.316635Z",
                "updated_at": "2018-07-11T18:02:28.667033Z",
                "cumulative_status": "problematic",
                "extent": null
            },
            {
                "id": 638,
                "guid": "d4623dfc-ab59-46c4-8647-2f1e1ef0443b",
                "name": "Australia - New South Wales - Topographic",
                "desc": "Cached Map Service of NSW showing roads, points of interest, localities, landform, drainage, cultural data, parks & forests, property boundaries and street address numbers. Metadata_link http://sdi.nsw.gov.au/catalog/search/resource/details.page?uuid=%7B7DF76070-8307-49A2-A381-3D9686EAFDDC%7D",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": "d06765ea-95dd-497d-8963-42ff5affa4fe",
                "created_at": "2016-11-25T20:00:37.885603Z",
                "updated_at": "2016-11-25T20:00:37.885603Z",
                "cumulative_status": "works",
                "extent": "SRID=4326;POLYGON ((140.9948644000000115 -37.8474136999999970, 159.4938303000000133 -37.8474136999999970, 159.4938303000000133 -27.6936059999999991, 140.9948644000000115 -27.6936059999999991, 140.9948644000000115 -37.8474136999999970))"
            },
            {
                "id": 637,
                "guid": "10df7a62-a447-4eb5-bbf4-040360d09b04",
                "name": "Australia - Tasmania LIST Orthophoto",
                "desc": "Tasmania State Orthophoto compilation. Coverage compiled from latest aerial photos sourced from DPIPWE, Southern Councils, and individual projects. The resolution of the raster capture varies, with many urban areas at a higher resolution.For Services Terms and Conditions, please see the LIST Web Services Terms and Conditions (http://listdata.thelist.tas.gov.au/public/LISTWebServicesTermsConditions.pdf)",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": "d06765ea-95dd-497d-8963-42ff5affa4fe",
                "created_at": "2016-11-25T19:54:24.700639Z",
                "updated_at": "2016-11-25T19:54:24.700639Z",
                "cumulative_status": "works",
                "extent": null
            },
            {
                "id": 636,
                "guid": "24f06d38-64ad-4467-b80d-82ad5cfc1cd1",
                "name": "Australia - Tasmania LIST Topographic",
                "desc": "Tasmania Topographic base map. Different map scales used to represent the map. Created from vector data.For Services Terms and Conditions, please see the LIST Web Services Terms and Conditions (http://listdata.thelist.tas.gov.au/public/LISTWebServicesTermsConditions.pdf)",
                "type": "tms",
                "epsg": 3857,
                "icon": null,
                "submitter": "d06765ea-95dd-497d-8963-42ff5affa4fe",
                "created_at": "2016-11-25T19:47:57.742223Z",
                "updated_at": "2016-11-25T19:47:57.742223Z",
                "cumulative_status": "works",
                "extent": null
            }
        ]
    }

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
