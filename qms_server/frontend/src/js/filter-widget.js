/**
 * Created by yellow on 4/19/16.
 */

import SearchEngine from "./search_engine"
import Handlebars from "handlebars"

if ($("#results").length){

  var element_template,
      no_result_template;

  // load templates
  $.get(element_template_url, function(source) {
          element_template = Handlebars.compile(source);
  });

  $.get(no_results_templ_url, function(source) {
          no_result_template = Handlebars.compile(source);
  });

  var foundService = 0;

  // renderer handler
  var render_services = function(data) {
      return new Promise(function(resolve, reject) {
          // clear
          $("#results").fadeOut(200, function () {
              $("#results").empty().show();

              foundService = 0;

              // render
              if (data.length < 1) {
                  var context = {};
                  var elem = no_result_template(context);
                  $(elem).hide().appendTo('#results').fadeIn(200);

                  $('#service-count')[0].innerText = foundService;
              }
              else {
                  $.each(data, function (index, service) {
                      var context = {
                          service: service,
                          service_desc: service.desc ? service.desc : "None",
                          service_epsg: service.epsg ? service.epsg : "None",
                          service_url: service_url.replace('%id', service.id),
                          icon_url: service.icon ? icon_url.replace('%id', service.icon) : default_icon_url,
                          updated_at: service.updated_at != null ? (new Date(service.updated_at)).toISOString().slice(0, 10) : "None",
                          my_service: user_guid && user_guid === service.submitter,
                          edit_url: edit_url.replace('%id', service.id)
                      };
                      var elem = element_template(context);
                      $(elem).hide().appendTo('#results').show();

                      foundService += 1;
                      $('#service-count')[0].innerText = foundService;
                  });
              }
              resolve();
          });
      });
  };

  // Create search control
  var searcher = new SearchEngine({
    url: "/api/v1/geoservices/",
    param: "search",
    delay: 50,
    on_success: render_services,
    default_order: '-updated_at'
  });

  searcher.addTextBox($("#txt_search").first());
  searcher.addFilterButton($("#flt_all").first(), "type", "");
  searcher.addFilterButton($("#flt_tms").first(), "type", "tms");
  searcher.addFilterButton($("#flt_wms").first(), "type", "wms");
  searcher.addFilterButton($("#flt_wfs").first(), "type", "wfs");
  searcher.addFilterButton($("#flt_geojson").first(), "type", "geojson");
  if(user_guid) {
      searcher.addFilterButton($("#flt_my").first(), "submitter", user_guid);
  }

  // update data
  $("#txt_search").keyup();
}
