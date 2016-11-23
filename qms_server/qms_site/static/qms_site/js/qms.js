// QMS add form
var QMSAddForm = (function(){
    var qmsAddForm = $(".qms-add-service");

    function isFormFilled(form){
        var result = false;
        form.find("input, select").each(function(){
            if ($(this).val()) {
                result = true;
                return false;
            }
        });
        return result;
    }

    var me = {
        init: function(){
            qmsAddForm.each(function(){
                var form = $(this),
                    licenseForm = form.find(".qms-add-service__license-form"),
                    licenseInfo = form.find(".qms-add-service__license-info");

                licenseForm.on("innerForm.save", function(){
                    console.log("innerForm.save")
                    if (isFormFilled(licenseForm)){
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