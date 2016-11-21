// QMS add form
var QMSAddForm = (function(){
    var qmsAddForm = $(".qms-add-service");

    var me = {
        init: function(){
            qmsAddForm.each(function(){
                var form = $(this),
                    licenseForm = form.find(".qms-add-service__license-form"),
                    licenseNameControl = licenseForm.find(".qms-add-service__license-name"),
                    licenseInfo = form.find(".qms-add-service__license-info");

                licenseForm.on("innerForm.save", function(){
                    if (licenseNameControl.val()){
                        licenseInfo.addClass("filled");
                    } else{
                        licenseInfo.removeClass("filled");
                    }
                })
            })
        }
    }

    if (qmsAddForm.length)
        me.init();

    return me;
})();