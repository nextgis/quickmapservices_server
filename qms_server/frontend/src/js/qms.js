// QMS add form
export default class QMSAddForm{
    constructor() {
      this.qmsAddForm = $(".qms-add-service");
      var that = this;

      if (qmsAddForm.length){
        qmsAddForm.each(function(){
            var form = $(this),
                licenseForm = form.find(".qms-add-service__license-form"),
                licenseInfo = form.find(".qms-add-service__license-info");

            licenseForm.on("innerForm.save", function(){
                if (that.isFormFilled(licenseForm)){
                    licenseInfo.addClass("filled");
                } else{
                    licenseInfo.removeClass("filled");
                }
            });

            form.on("submit", function(e){
                if (form.valid()) {
                    if (!that.isFormFilled(licenseForm)) {
                        return confirm(noLicenseConfirmText);
                    } else {
                        return true;
                    }
                } else {
                    return false;
                }
            });
        })
      }
    }

    isFormFilled(form){
        var result = false;
        form.find("input, select").each(function(){
            if ($(this).val()) {
                result = true;
                return false;
            }
        });
        return result;
    }
}
