import L from 'leaflet'
import 'proj4leaflet'
import 'leaflet-wfst/dist/Leaflet-WFST.src'

var MAPID = 'mapid';

var mapWrapper = document.getElementById(MAPID);

if (mapWrapper) {

  /**
   * Add preview layer to the map.
   * if the layer is overlay, add a base layer as well
   * @param {Object} data
   * @param {L.Layer} [data.previewLayer]
   * @param {boolean} [data.baseLayer]
   */
  var buildMap = function (data) {

    var previewMap = new L.Map('mapid').setView([55, 44], 2);

    var createBaseLayer = function () {
      return new L.TileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
      });
    }
    if (data.baseLayer) {
      createBaseLayer().addTo(previewMap);
    }
    if (data.previewLayer) {
      data.previewLayer.addTo(previewMap);

      var fitBounds = function () {
        if (data.previewLayer.getBounds) {
          previewMap.fitBounds(data.previewLayer.getBounds());
        }
      }

      fitBounds();

      data.previewLayer.once('load', fitBounds);
    }
  }

  /**
   *
   * @param {Object} opt - service data
   */
  var getData = function (opt) {

    return new Promise(function (resolve, reject) {

      var crs = (opt.epsg == 3857 || opt.epsg == 4326 || opt.epsg == 3395) ?
        L.CRS["EPSG" + opt.epsg] : undefined;

      if (opt.type === 'geojson') {

        $.ajax({
          // url: opt.geojson.url,
          url: '/geoservices/' + service.id + '/data',
          dataType: 'json',
          type: 'GET',
          contentType: "application/json",
          success: function (response) {
            var data = response && response.data;
            if (data) {
              resolve({
                previewLayer: L.Proj.geoJson(JSON.parse(data), {
                    style: { color: 'blue', weight: 2 }
                  }),
                  baseLayer: true
                })
            } else {
              reject(response.error_text || "could not load geojson data")
            }
          },
          error: function (jqXHR, exception) {
            reject(exception);
          }
        });
      } else {

        var previewLayer;
        var baseLayer = true;

        if (opt.type === 'tms') {
          baseLayer = false;
          previewLayer = new L.TileLayer(opt.tms.url, {
            minZoom: opt.tms.zmin,
            maxZoom: opt.tms.zmax,
          })
        } else if (opt.type === 'wms') {
          previewLayer = new L.TileLayer.WMS(opt.wms.url, {
            layers: opt.wms.layers,
            transparent: true,
            crs: crs,
            format: opt.wms.format
          })
        } else if (opt.type === 'wfs') {
          previewLayer = new L.WFS({
            url: opt.wfs.url,
            style: {
              color: 'blue',
              weight: 2
            },
            typeName: opt.wfs.typeName,
            typeNS: opt.wfs.typeNS,
            crs: crs
          })
        }
        if (previewLayer) {
          resolve({ baseLayer: baseLayer, previewLayer: previewLayer });
        } else {
          reject(opt.type + " is not supported layer type");
        }
      }
    })
  }

  getData(service).then(buildMap).catch(function (er) {
    console.error(er)
    mapWrapper.innerHTML = "Preview is not available"
  })
}
