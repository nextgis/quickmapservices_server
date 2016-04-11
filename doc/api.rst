.. sectionauthor:: Дмитрий Барышников <dmitry.baryshnikov@nextgis.ru>


NextGIS QMS Service API
=======================

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
            "id": 90,
            "guid": "b72b43e3-8793-42bb-8d03-3dc29f896010",
            "name": "NASA SEDAC Earthquake Hazard Frequency and Distribution",
            "desc": null,
            "type": "wms",
            "epsg": null
        },
        {
            "id": 91,
            "guid": "8c4d011a-a908-4738-abf5-c757078ac8bb",
            "name": "NASA Fires - Past 48 hours",
            "desc": null,
            "type": "wms",
            "epsg": null
        },
        {
            "id": 92,
            "guid": "f9536cde-d6cc-4b89-91f5-d95117b0e36a",
            "name": "MapSurfer ASTER GDEM contour lines",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 93,
            "guid": "f02ae29e-68d8-40e4-a4be-e40af70c0c8c",
            "name": "MapSurfer OSM Roads",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 94,
            "guid": "cc12411a-e12d-4bc9-9d9f-9a91736e29c9",
            "name": "NASA SEDAC Earthquake Hazard Distribution - Peak Ground Acceleration",
            "desc": null,
            "type": "wms",
            "epsg": null
        },
        {
            "id": 95,
            "guid": "eb259a30-fd24-4bbe-92a8-5883657c1556",
            "name": "OSM TF Transport Dark",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 96,
            "guid": "e4b25632-b47b-4818-b8d0-7678f6e84902",
            "name": "MapSurfer OSM Roads Grayscale",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 97,
            "guid": "ecea536d-67ae-4f0e-809d-99bb52973408",
            "name": "MapSurfer ASTER GDEM-SRTM Hillshade",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 99,
            "guid": "1d65b52b-fa18-4812-8bd2-2fda94cc79a7",
            "name": "OSM TF Outdoors",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 100,
            "guid": "7549f406-2ed0-451c-bb40-346704fac065",
            "name": "OSM TF Landscape",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 101,
            "guid": "24f90281-90ea-4771-b186-46f2625aa938",
            "name": "OSM TF OpenCycleMap",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 102,
            "guid": "1ad55195-2099-46f5-89fd-895171dcf988",
            "name": "Rosreestr Cadastre",
            "desc": null,
            "type": "wms",
            "epsg": null
        },
        {
            "id": 103,
            "guid": "691647c0-d24a-4752-b7f9-3aab007b3323",
            "name": "Rosreestr BaseMap Annotations",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 104,
            "guid": "bd2de095-7482-461a-96d5-fd9695eb8439",
            "name": "OSM TF Transport",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 105,
            "guid": "cd56bbe7-dc1b-4a79-99fa-e77c94481e43",
            "name": "Rosreestr BaseMap",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 106,
            "guid": "02fa1fdf-d1bd-45b0-a0d0-6b5742017252",
            "name": "NASA Fires - Past 24 hours",
            "desc": null,
            "type": "wms",
            "epsg": null
        },
        {
            "id": 107,
            "guid": "50f32729-152a-4c8f-9631-c4ddc92c78cb",
            "name": "MapQuest Aerial",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 108,
            "guid": "c2d35052-9348-4d8d-a289-f1956384cb52",
            "name": "MapSurfer OSM Semitransparent",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 109,
            "guid": "8e7fa73c-6f30-4e59-8517-389fb3165d78",
            "name": "MapQuest OSM",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 110,
            "guid": "c0fec193-52f3-408d-be20-ebebbd1e28d2",
            "name": "MapSurfer OSM Administrative Boundaries",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 111,
            "guid": "12fa8a7d-398e-48cf-af28-afada8fdde36",
            "name": "Google Road",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 112,
            "guid": "e984f04d-2dbe-4a26-aa74-9c23611dd1a4",
            "name": "ESRI Gray (light)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 113,
            "guid": "c8798bfa-b7d3-4848-88df-38af00bf0ff4",
            "name": "Ukraine cadastre Topo",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 114,
            "guid": "fa3fc808-9dcf-409a-b369-e4b4ae88f88d",
            "name": "2gis Map",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 115,
            "guid": "15307d61-67b5-4a81-92d0-35524f13902e",
            "name": "Kosmosnimki.ru Satellite",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 116,
            "guid": "43c6fe2f-7394-402f-ae33-9be9825ca705",
            "name": "Yandex Satellite",
            "desc": null,
            "type": "tms",
            "epsg": 3395
        },
        {
            "id": 117,
            "guid": "ea28efbb-f2c3-4c20-b2dd-6ff2b4309964",
            "name": "ESRI Reference Overlay",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 118,
            "guid": "7cbe4131-1d60-4527-8f00-bea3e6e5fdc0",
            "name": "Google Labels",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 119,
            "guid": "7acd8ca9-2ed5-4829-b08f-f7312bc515a4",
            "name": "Bing Map",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 120,
            "guid": "f5f76700-a1f3-454e-bb95-2c8736e5cce4",
            "name": "Positron (retina)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 121,
            "guid": "cab9e57b-2b19-4644-b3f9-f915ee4dcdaf",
            "name": "Google Traffic",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 122,
            "guid": "8bd167ce-13b1-44c2-821f-33498a458913",
            "name": "Dark Matter [no labels]",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 123,
            "guid": "5fb37916-02d4-4644-a951-2ef1a45a4d6d",
            "name": "ESRI Shaded Relief",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 124,
            "guid": "29654bc6-d3b0-48d9-b998-bd47048fb124",
            "name": "Topomap (marshruty.ru)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 125,
            "guid": "693a59a7-cb80-4aa0-90c4-75ac842a9e80",
            "name": "ESRI Transportation",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 126,
            "guid": "a61bf935-e313-4734-a9db-a7a5790614d7",
            "name": "Yandex Narod Map",
            "desc": null,
            "type": "tms",
            "epsg": 3395
        },
        {
            "id": 127,
            "guid": "da8bfba1-925b-4502-ad6a-71ae2a7f2449",
            "name": "ESRI Ocean",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 128,
            "guid": "50b9845a-d61a-48a0-8b6a-38384bdbfbd0",
            "name": "Genshtab 250m",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 129,
            "guid": "24dc8eb0-3da1-4bf4-8b36-b436734e78b7",
            "name": "Stamen Toner Background",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 130,
            "guid": "4e008afc-ff96-4379-9ae0-5e49e3dc3f88",
            "name": "ESRI Gray (dark)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 131,
            "guid": "62b98a00-1e8c-45df-896a-cee301387714",
            "name": "Dark Matter [no labels] (retina)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 132,
            "guid": "2cc6440b-d4cc-4deb-bbc0-6c95011ea2a7",
            "name": "Dark Matter (retina)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 133,
            "guid": "82d9950f-b08b-4592-8b7c-da8dbaa1c607",
            "name": "OpenStreetMap monochrome",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 134,
            "guid": "69c01601-cc39-481a-9e70-1015403195a5",
            "name": "Google Satellite",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 135,
            "guid": "24af2200-c77a-4a2b-9534-3d0c13e50358",
            "name": "NG NAPR STREETS",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 136,
            "guid": "14ef68f3-e76c-46a4-b3bd-a90966003819",
            "name": "bergfex osm",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 137,
            "guid": "ac8c5e92-cd55-4ca8-866f-ca59b22f2fda",
            "name": "Sputnik Map",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 138,
            "guid": "95142dbe-259d-4656-a1a0-1087e00c3183",
            "name": "Positron",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 139,
            "guid": "d7008d4b-5495-42cf-889a-42fbbc4fc221",
            "name": "Ukraine cadastre OrtoPhoto",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 140,
            "guid": "0f6e9441-4241-41c9-9de8-abd3a061d4c4",
            "name": "Stamen Toner (Retina)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 141,
            "guid": "45e3a75b-859d-4253-9453-e38a1731473b",
            "name": "Mapbox Satellite",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 142,
            "guid": "e740b3a3-5492-4641-aff2-65767743c387",
            "name": "Kosmosnimki.ru Map",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 143,
            "guid": "a15ff108-1df0-4177-99e1-660a2e4baf08",
            "name": "Positron [no labels]",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 144,
            "guid": "d27b402c-475f-44b9-a6d7-5a50a671890c",
            "name": "bergfex oek",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 145,
            "guid": "ecf6ff52-8549-4b4b-ac0c-384f466148fb",
            "name": "ESRI Satellite",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 146,
            "guid": "ab61ebd0-71c8-4bb1-9828-b2692c4bc1ef",
            "name": "ESRI Physical",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 147,
            "guid": "83e8ef65-5094-4b50-b1cd-8adeb9b82bac",
            "name": "Genshtab (in7ane.com)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 148,
            "guid": "76f6bec4-5f16-4b3a-97e7-8928cfb471f8",
            "name": "ESRI National Geographic",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 149,
            "guid": "b085697d-6a34-4ec7-80ba-1f670c8aa3fd",
            "name": "Openstreetmap tracks",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 150,
            "guid": "c68f2c53-7aa7-4b87-b069-4b6872747406",
            "name": "Kosmosnimki.ru Terrain",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 151,
            "guid": "13dea7b4-276a-4ad7-8591-ff81a77231e5",
            "name": "ESRI Boundaries&Places",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 152,
            "guid": "9bc04942-cfe8-43ba-a824-eb611c9c9360",
            "name": "Kosmosnimki.ru Overlay",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 153,
            "guid": "d69c273a-dcce-4f91-84f2-7e3d1202ba02",
            "name": "Mapbox Gray",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 154,
            "guid": "931905b8-89fe-44d4-9bf1-3edfbab86afb",
            "name": "Stamen Toner Lite",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 155,
            "guid": "37ebcfbb-e828-4cac-8ec9-51ed76d70101",
            "name": "OpenTopoMap",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 156,
            "guid": "19996282-3680-4411-a1c0-dce64675ffee",
            "name": "Google Terrain",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 157,
            "guid": "a57e10ef-7be5-49e3-866b-414495603fa3",
            "name": "Genshtab 500m",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 158,
            "guid": "e4c459a6-3a9c-45fa-adc4-d113d54caf7e",
            "name": "ESRI Standard",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 159,
            "guid": "09f7666c-b184-43cd-a067-bd30e26a1c64",
            "name": "OSM2World/3D (D,A,CH)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 160,
            "guid": "c01b2dfb-5f09-4cd6-a340-345df91b680f",
            "name": "Waze (World)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 161,
            "guid": "e9ca0298-c6fc-433c-9e17-991d330f5ce8",
            "name": "Google Hybrid",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 162,
            "guid": "5b3859f6-60e6-40d3-a4b9-4f1c0a93ab44",
            "name": "Stamen Watercolor",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 163,
            "guid": "ab742247-cc6d-471e-b23c-27794f30e68b",
            "name": "Waze (US)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 164,
            "guid": "d6c5b4f2-06f1-4cb2-bed9-5c7cd75642e9",
            "name": "Stamen Toner Labels",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 165,
            "guid": "780ce6ee-afe0-4ed0-8cb2-345634015f39",
            "name": "Positron [no labels] (retina)",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 166,
            "guid": "307a1b52-d74b-4dd3-ba4a-c0b82135ab85",
            "name": "ESRI Topo",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 167,
            "guid": "c90938aa-5085-4f38-9179-388188907ecd",
            "name": "ESRI Terrain",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 168,
            "guid": "67ce318c-03dc-4d84-8fa1-f800768830c7",
            "name": "Bing Map Ru",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 169,
            "guid": "209f26a6-935b-43ea-a33a-427845f68ac9",
            "name": "Stamen Toner Hybrid",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 170,
            "guid": "95a79bfe-b966-4a80-a844-63f8f54532b4",
            "name": "Yandex Map",
            "desc": null,
            "type": "tms",
            "epsg": 3395
        },
        {
            "id": 171,
            "guid": "b891d96b-171c-477e-a873-00d4ec5de91d",
            "name": "Wikimedia Map",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 172,
            "guid": "661f74ef-55fb-4b64-acf5-47608c9bc1bc",
            "name": "Bing Satellite",
            "desc": null,
            "type": "tms",
            "epsg": 3857
        },
        {
            "id": 173,
            "guid": "00606686-2d23-4bc1-9740-19d2ccbe90db",
            "name": "Stamen Toner",
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

