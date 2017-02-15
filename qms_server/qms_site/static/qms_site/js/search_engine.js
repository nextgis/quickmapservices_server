function SearchEngine(config) {
    this._settings = $.extend(true, this.default_config, config || {});
    this._editBox = null;
    this._filterButtons = [];
    this._activeFilters = {};
}

SearchEngine.prototype.default_config = {
    url: '/search',
    param: 'query',
    on_success: null,
    delay: 500,
    loading_css: '#loading',
    default_order: 'name',
    search_order: 'name'
};

SearchEngine.prototype.loading = function () {
    $(this._settings.loading_css).show();
};

SearchEngine.prototype.idle = function () {
    $(this._settings.loading_css).hide();
};

SearchEngine.prototype.start = function () {
    $(document).trigger('before.searchbox');
    this.loading();
};

SearchEngine.prototype.stop = function () {
    this.idle();
    $(document).trigger('after.searchbox')
};

SearchEngine.prototype.resetTimer = function (timer) {
    if (timer) clearTimeout(timer);
};

SearchEngine.prototype.process = function () {
    var req_params = $.extend({}, this._activeFilters),
        that = this;
    req_params[this._settings.param] = this._editBox.val();
    if(!this._editBox.val())
        req_params['ordering'] = this._settings.default_order;
    else
        req_params['ordering'] = this._settings.search_order;
    $.get(this._settings.url, req_params, $.proxy(function (data) {
         this._settings.on_success(data).then(function(){
            that.stop();
         });
    }, this));
};

SearchEngine.prototype.addTextBox = function (control) {
    this._editBox = control;
    control
        .focus()
        .keyup($.proxy(function () {
            if (control.val() != this._previousValue) {
                this.resetTimer(this._timer);

                this._timer = setTimeout($.proxy(function () {
                    this.start();
                    this.process();
                }, this), this._settings.delay);

                this._previousValue = control.val();
            }
        }, this));
};

SearchEngine.prototype.addFilterButton = function (control, filter_name, filter_val) {
    this._filterButtons.push(control);
    control
        .click( $.proxy(function (e) {
            e.preventDefault();

            this._activeFilters = {}; //TODO: single filter!
            this._activeFilters [filter_name] = filter_val; // set value

            $.each(this._filterButtons, function(index, el) {
                el.removeClass('active');
            });
            control.addClass('active'); //change css

            // update
            this.resetTimer(this._timer);
            this._timer = setTimeout($.proxy(function () {
                    this.start();
                    this.process();
            }, this), this._settings.delay);
        }, this));
};
