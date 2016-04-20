/**
 * Created by yellow on 4/19/16.
 */

//Add search by cities
citys_bh = new Bloodhound({
    datumTokenizer: function (d) {
        return Bloodhound.tokenizers.whitespace(d.name);
    },
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    remote: {
        url: 'http://rgada.info/nextgisweb/resource/875/store/?like=%QUERY',
        wildcard: '%QUERY'
    }
});

citys_bh.initialize();

all_data_sources.push({
        name: 'city',
        display: 'name',
        source: cityMinLengthFilter,
        templates: { header: '<h3>Поселения</h3>' }
});


// Create search control
$('#bloodhound .typeahead').typeahead({
        hint: true,
        highlight: true,
        minLength: 1
    },
	  all_data_sources
    ).on("typeahead:selected", function (obj, datum) {
        if(datum.hasOwnProperty('MendeName')) { // bad check !
            showCityPopup(datum);
        }
        else {
            showPopupById(datum.id);
        }
    }).on("change", function(event) {
        popup.hide();
    });

