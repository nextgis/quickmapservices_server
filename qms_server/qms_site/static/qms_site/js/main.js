// Authorization and registration panel module
var AuthPanel = (function() {
    var authPanel = $(".auth-panel");

    var result = {
        init: function(){
            var close = authPanel.find(".js-close");
            if (close.length)
                close.on("click", function(e){
                    result.close();
                });
        },
        show: function(target) {
            var content = authPanel.find(target);
            if (content.length){
                content.siblings(".active").hide().removeClass("active");
                content.addClass("active").fadeIn().css("display","inline-block");
            }

            if (authPanel.is(":hidden"))
                authPanel.fadeIn();
        },
        close: function() {
            if (authPanel.is(":visible"))
                authPanel.fadeOut();
        }
    };
    return result;
})();

// Forms module
var Forms = (function(){
    var forms = $("form");
    var validateForms =$(".form-validate");

    function initValidator(){
        $.validator.addMethod("equal", function(value, element) {
            var equalTo=$($(element).data("equalto"));
            if ( equalTo.not( ".validate-equalTo-blur" ).length ) {
                equalTo.addClass( "validate-equalTo-blur" ).on( "blur.validate-equalTo", function() {
                    $( element ).valid();
                });
            }
            return value === equalTo.val();
        }); 
    }

    function fixAutofill(){
        setTimeout(function(){
            if ($(":-webkit-autofill").length)
                $(":-webkit-autofill").parents(".form-group.is-empty").removeClass("is-empty");
        }, 100)
        
    }

    function clearErrors(form, el){
        var id = form.attr("id");
        
        $(".alert:visible[data-form="+ id + "]").fadeOut(function(){
            $(this).remove();
        });

        if (el){
            el.parents(".form-group.has-error").removeClass("has-error");
            el.siblings("span.has-error").remove();   
        }
    }

    return {
        init: function(){
            fixAutofill();
            initValidator();

            forms.each(function(){
                var form = $(this);

                // Hide alert and errors on change form
                form.find('.form-control').on('keyup', function(){
                    clearErrors(form, $(this));
                });

                form.find('[type=submit]').on('click', function(){
                    clearErrors(form);
                });
            });

            validateForms.each(function(){
                var form = $(this);
                var id=$(this).attr("id");

                //validate                 
                form.validate({
                    errorClass: "has-error",
                    errorElement:"span",
                    highlight: function(element, errorClass, validClass) {
                        if ( element.type === "radio" ) {
                            this.findByName( element.name ).addClass( errorClass ).removeClass( validClass );
                        } else {
                            $( element ).addClass( errorClass ).removeClass( validClass );
                            $(element).parents(".form-group").addClass(errorClass);
                        }
                    },
                    errorPlacement: function(error, element) {
                        element.parent().append(error);
                    },
                    unhighlight: function( element, errorClass, validClass ) {
                        if ( element.type === "radio" ) {
                            this.findByName( element.name ).removeClass( errorClass ).addClass( validClass );
                        } else {
                            $( element ).removeClass( errorClass ).addClass( validClass );
                            $( element ).parents(".form-group."+ errorClass).removeClass(errorClass);
                        }
                    }
                });
            })
        }
    }
})();

// Messages module
var Messages = (function(){
    return {
        init: function(){
            if ($(".alert--timeout").length){
                $(".alert--timeout").each(function(){
                    var alert=$(this);
                    setTimeout(function(){
                        alert.fadeOut(function(){
                            alert.remove();
                        });
                    }, 5000);
                })
            }
        }
    }
})();

// Dynamic fields
var DynamicFieds =(function(){
    var fields = $(".form-control--dynamic");

    function clearTarget(el){
        el.each(function(){
            $(this).find(".form-control").val("").change();
        })
    }

    return {
        init: function(){
            fields.each(function(){
                var me = $(this);
                var target = $(me.data("relative-field")).parents(".form-group").hide();

                me.on("keyup paste", function(){
                    if (me.val() != "")
                        target.each(function(){
                            $(this).slideDown()
                        })
                    else
                        target.each(function(){
                            $(this).slideUp(function(){
                                clearTarget($(this));
                            });
                        });
                })
            })
        }
    }
})();

// Service menu
var Nav = (function(){
    var menuLink = $(".js-service-menu"),
        menu = $(".nav__service-menu"),
        nav = $(".nav"),
        overlay = $(".overlay");

    function checkBordered(){
        if ($(window).scrollTop() < 100){
            if (!menu.is(":visible")) result.unborderedNav();
        } else
            result.borderedNav();
    }

    function scrollWatcher(){
        checkBordered();
        $(window).on("scroll", function(){
            checkBordered()
        });
    }

    var result =  {
        init: function(){
            scrollWatcher();

            if (menu.length){
                menuLink.on("click", function(){
                    if (menu.is(":visible"))
                        result.hideMenu()
                    else
                        result.showMenu();
                    return false;
                })

                overlay.on("click", function(){
                    result.hideMenu();
                })
            } 
        },       
        showMenu: function(){
            menu.slideDown(150, function(){
                result.borderedNav();
            });
            menuLink.addClass("shown");
            overlay.fadeIn(150);
        },
        hideMenu: function(){
            menu.slideUp(150, function(){
                checkBordered();
            });
            menuLink.removeClass("shown");
            overlay.fadeOut(150);
        },
        borderedNav: function(){
            nav.addClass("bordered");
        },
        unborderedNav: function(){
            nav.removeClass("bordered");
        }
    }

    return result;
})();

$(document).ready(function(){
    svg4everybody();
    $.material.init();

    // Fixed nav
    if ($(".nav--fixed").length){
        Nav.init();
    }

    // Athorization and registration panel
    if ($(".auth-panel").length){        
        AuthPanel.init();
        $(".js-authPanel").on("click", function(e){
            var target=$(this).attr("href");
            if (target) AuthPanel.show(target);
            e.preventDefault();
        });
    }

    // Forms
    if ($("form").length)
        Forms.init();

    // Messages
    if ($(".alert").length)
        Messages.init();

    // Customize select
    if ($(".select").length)
        $(".select").dropdown({ "autoinit" : "select" });

    //Dynamic fields
    if ($(".form-control--dynamic").length)
        DynamicFieds.init();

});