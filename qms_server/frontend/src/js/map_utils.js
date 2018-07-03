import {Util} from 'leaflet';

export function prepareWmsUrl(url) {

  var params = {};
  var correctparams = {};
  url.replace(/[?&]+(\w+)([^&]*)/gi, (m, key) => {
    params[key] = true;
    return key;
  });
  url = url.replace(/[?&]+([^=&]+)=([^&]*)/gi, (m, key, value) => {
    params[key] = decodeURIComponent(value);
    return "";
  });

  for (var p in params) {
    if (params.hasOwnProperty(p)) {
      var param = params[p];
      if (typeof param === 'string') {

      }
      var paramWithBraces = param.match(/\{ *([\w_-]+) *\}/);
      if (!paramWithBraces) {
        correctparams[p] = param;
      }
    }
  }

  // url = url.replace(/=\{ *([\w_-]+) *\}/g, ""); // [?&]+((\w+)\=\{ *([\w_-]+) *\})([^&]*)
  return url + Util.getParamString(correctparams, url);
}
