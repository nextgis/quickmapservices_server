import {getURLParameter} from '@nextgis_common/js/utilities'


$(window).on('load',function(){
    var reportPopup = $(".report-problem-popup"),
        reportForm = reportPopup.find("form");

    reportPopup.modal();
    reportPopup.on('show.bs.modal', function (e) {
        reportForm.find("select").change();
    });
    
    if (getURLParameter("show-report-problem")) {
        $('[data-target=".report-problem-popup"]').click();
    }

    function clearReport() {
        reportForm.find("input,select,textarea").each(function () {
            this.value = "";
            $(this).change();
            $(this).valid();
        });
        reportForm.validate().resetForm();
    }

});
