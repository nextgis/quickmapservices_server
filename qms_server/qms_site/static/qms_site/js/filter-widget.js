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


var total=0, wms=0, wfs=0, geojson=0, tms=0, my=0;

function reset_counters() {
    total=0, wms=0, wfs=0, geojson=0, tms=0, my=0;
    $('#flt_all_count')[0].innerText = "";
    $('#flt_wms_count')[0].innerText = "";
    $('#flt_wfs_count')[0].innerText = "";
    $('#flt_tms_count')[0].innerText = "";
    $('#flt_geojson_count')[0].innerText = "";
    //$('#flt_my_count')[0].innerText = "";
}

function update_counters() {
    $('#flt_all_count')[0].innerText = total != 0 ? "[" + total + "]" : "" ;
    $('#flt_wms_count')[0].innerText = wms != 0 ? "[" + wms + "]" : "" ;
    $('#flt_wfs_count')[0].innerText = wfs != 0 ? "[" + wfs + "]" : "" ;
    $('#flt_tms_count')[0].innerText = tms != 0 ? "[" + tms + "]" : "" ;
    $('#flt_geojson_count')[0].innerText = geojson != 0 ? "[" + geojson + "]" : "" ;
    //$('#flt_my_count')[0].innerText = my != 0 ? "[" + my + "]" : "" ;
}

// renderer handler
render_services = function(data) {
    // clear
    $("#results").fadeOut(200, function () {
        $("#results").empty().show();
    reset_counters();

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
                icon_url: service.icon ? icon_url.replace('%id', service.icon) : default_icon_url,
                updated_at: service.updated_at!=null ? (new Date(service.updated_at)).toISOString().slice(0, 10) : "None",
                my_service: user_guid && user_guid===service.submitter,
                edit_url: edit_url.replace('%id', service.id)
            };
            var elem    = element_template(context);
            $(elem).hide().appendTo('#results').fadeIn(200);

            if (service.type == 'wms') {
                wms += 1;
            }
            total += 1;
            update_counters();
        });
    }

    });
};

// Create search control
searcher = new SearchEngine({
  url: "/api/v1/geoservices/",
  param: "search",
  delay: 500,
  on_success: render_services,
  default_order: '-id'
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
