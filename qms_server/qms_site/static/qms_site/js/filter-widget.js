/**
 * Created by yellow on 4/19/16.
 */

// load templates
$.get(element_template_url, function(source) {
        element_template = Handlebars.compile(source);
});

$.get(no_results_templ_url, function(source) {
        no_result_template = Handlebars.compile(source);
});

// renderer handler
render_services = function(data) {
    // clear
    $("#results").fadeOut(200, function () {
        $("#results").empty().show();

    // render
    if(data.length < 1) {
        var context = {};
        var elem    = no_result_template(context);
        $(elem).hide().appendTo('#results').fadeIn(200);
    }
    else {
        $.each(data, function (index, service) {
            var context = {
                service: service,
                service_desc: service.desc ? service.desc : "None",
                service_epsg: service.epsg ? service.epsg : "None",
                service_url: service_url.replace('%id', service.id),
                icon_url: service.icon ? icon_url.replace('%id', service.icon) : default_icon_url
            };
            var elem    = element_template(context);
            $(elem).hide().appendTo('#results').fadeIn(200);
        });
    }

    });
};

// Create search control
searcher = new SearchEngine({
  url: "/api/v1/geoservices/",
  param: "search",
  delay: 500,
  on_success: render_services
});

searcher.addTextBox($("#txt_search").first());
searcher.addFilterButton($("#flt_all").first(), "type", "");
searcher.addFilterButton($("#flt_tms").first(), "type", "tms");
searcher.addFilterButton($("#flt_wms").first(), "type", "wms");
searcher.addFilterButton($("#flt_wfs").first(), "type", "wfs");
searcher.addFilterButton($("#flt_geojson").first(), "type", "geojson");

// update data
$("#txt_search").keyup();
