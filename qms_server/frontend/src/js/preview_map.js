import L from 'leaflet'
import 'proj4leaflet'
import 'leaflet-wfst/dist/Leaflet-WFST.src'
import { prepareWmsUrl } from './map_utils';

import "leaflet/dist/leaflet.css";

// stupid hack so that leaflet's images work after going through webpack
import marker from 'leaflet/dist/images/marker-icon.png';
import marker2x from 'leaflet/dist/images/marker-icon-2x.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: marker2x,
  iconUrl: marker,
  shadowUrl: markerShadow
});

var MAPID = 'mapid';

var mapWrapper = document.getElementById(MAPID);

if (mapWrapper) {

  var createBaseLayer = function () {
    return new L.TileLayer("http://{s}.tile.osm.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });
  }

  /**
   * Add preview layer to the map.
   * if the layer is overlay, add a base layer as well
   * @param {Object} data
   * @param {L.Layer} [data.previewLayer]
   * @param {string} [data.name]
   * @param {string} [data.id] - service pk
   * @param {string} [data.boundary] - geojson
   */
  var buildMap = function (data) {

    var baseMaps = {};
    var overlayMaps = {};

    var previewMap = new L.Map(MAPID).setView([55, 44], 2);

    var baseLayer = createBaseLayer().addTo(previewMap);
    baseMaps['Empty'] = new L.TileLayer('');
    baseMaps['OSM'] = baseLayer;

    if (data.previewLayer) {
      data.previewLayer.addTo(previewMap);
      overlayMaps[data.name] = data.previewLayer;

      var fitBounds = function () {
        return new Promise(function (resolve) {
          var fitLayerBounds = function (boundary) {
            boundary = boundary || data.previewLayer;
            if (boundary.getBounds) {
              previewMap.fitBounds(boundary.getBounds());
            }
            resolve();
          }

          var applyBoundary = function (geojson) {
            if (geojson) {
              var boundary = new L.GeoJSON(geojson, { color: "red", fillOpacity: 0 }).addTo(previewMap);
              if (boundary && boundary.getBounds)
                overlayMaps["Boundary"] = boundary;
              fitLayerBounds(boundary);
            } else {
              fitLayerBounds()
            }
          }

          if (data.boundary) {
            applyBoundary(JSON.parse(data.boundary));
          }
          // obsolete condition
          // else {
          //   $.ajax({
          //     url: '/geoservices/' + data.id + '/boundary',
          //     dataType: 'json',
          //     type: 'GET',
          //     success: applyBoundary,
          //     error: fitLayerBounds
          //   });
          // }
        });

      }

      fitBounds().then(function () {
        L.control.layers(baseMaps, overlayMaps).addTo(previewMap);
      });
      data.previewLayer.once('load', fitBounds);
    }
  }

  /**
   *
   * @param {Object} opt - service data
   */
  var getPreviewLayer = function (opt) {

    return new Promise(function (resolve, reject) {

      var toReturn = Object.assign({}, opt);

      var crs = (opt.epsg == 3857 || opt.epsg == 4326 || opt.epsg == 3395) ?
        L.CRS["EPSG" + opt.epsg] : undefined;

      if (opt.type === 'geojson') {

        $.ajax({
          // url: opt.geojson.url,
          url: '/geoservices/' + opt.id + '/data',
          dataType: 'json',
          type: 'GET',
          contentType: "application/json",
          success: function (response) {
            var data = response && response.data;
            if (data) {
              resolve(Object.assign(toReturn, {
                previewLayer: L.Proj.geoJson(JSON.parse(data)),
              }
              ));
            } else {
              reject(response.error_text || "could not load geojson data");
            }
          },
          error: function (jqXHR, exception) {
            reject(exception);
          }
        });
      } else {

        var previewLayer;

        if (opt.type === 'tms') {
          previewLayer = new L.TileLayer(opt.tms.url, {
            minZoom: opt.tms.zmin,
            maxZoom: opt.tms.zmax,
          })
        } else if (opt.type === 'wms') {
          var wmsLayerParam = {
            layers: opt.wms.layers,
            transparent: true,
          };
          if (crs) {
            wmsLayerParam.crs = crs;
          }
          if (opt.wms.format) {
            wmsLayerParam.format = opt.wms.format;
          }
          var url = prepareWmsUrl(opt.wms.url);
          previewLayer = new L.TileLayer.WMS(url, wmsLayerParam)
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
          resolve(Object.assign(toReturn, { previewLayer: previewLayer }));
        } else {
          reject(opt.type + " is not supported layer type");
        }
      }
    })
  }

  getPreviewLayer(service)
    .then(buildMap)
    .catch(function (er) {
      console.error(er)
      mapWrapper.innerHTML = "Preview is not available"
    })
}
