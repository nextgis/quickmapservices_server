// QMS add form
import Vue from 'vue'
import FileUploader from '../components/FileUploader'

export default class QMSAddForm{
    constructor() {
      this.qmsAddForm = $(".qms-add-service");
      var that = this;

      if (this.qmsAddForm.length){
        this.qmsAddForm.each(function(){
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

            /* Service boundaries uploader*/

            new Vue({
              el: form[0].querySelector(".file-uploader"),
              template: '<file-uploader name="boundary"/>',
              components: { FileUploader }
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
