import L from 'leaflet'
import 'proj4leaflet'
import 'leaflet-wfst/dist/Leaflet-WFST.src'

if ($("#mapid").length){
  var preview_map = L.map('mapid').setView([55, 44], 2);

  if (service.type == 'tms') {
      L.tileLayer(service.tms.url, {
          minZoom: service.tms.zmin,
          maxZoom: service.tms.zmax,
      }).addTo(preview_map);
  } else if (service.type == 'wms') {
      L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png",
              {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}
      ).addTo(preview_map);

      L.tileLayer.wms(service.wms.url, {
          layers: service.wms.layers,
          transparent: true,
          crs: (service.epsg == 3857 || service.epsg == 4326 || service.epsg == 3395) ? L.CRS["EPSG" +service.epsg] : undefined,
          format: service.wms.format
      }).addTo(preview_map);
  } else if (service.type == 'wfs') {
      L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png",
              {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}
      ).addTo(preview_map);

      var wfs_lyr = new L.WFS({
          url: service.wfs.url,
          style: {
            color: 'blue',
            weight: 2
          },
          typeName: service.wfs.typeName,
          typeNS:  service.wfs.typeNS,
          crs: (service.epsg == 3857 || service.epsg == 4326 || service.epsg == 3395) ? L.CRS["EPSG" +service.epsg] : undefined
        }).addTo(preview_map)
          .once('load', function () {
            preview_map.fitBounds(wfs_lyr);
          });
  } else if (service.type == 'geojson'){
      L.tileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png",
              {attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'}
      ).addTo(preview_map);

      $.ajax({
          url: service.geojson.url,
          dataType: 'json',
          success: function (response) {
              geojson_lyr = L.Proj.geoJson(response, {
                  style: { color: 'blue', weight: 2 }
              }).addTo(preview_map)
              .once('load', function () { preview_map.fitBounds(geojson_lyr); });
          }
      });
  }
}
