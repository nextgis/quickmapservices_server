function SearchEngine(config) {
    this._settings = $.extend(true, this.default_config, config || {});

}

SearchEngine.prototype.default_config = {
    url: '/search',
    param: 'query',
    dom_id: '#results',
    result_f: null,
    delay: 100,
    loading_css: '#loading'
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
    if (timer) clearTimeout(timer)
};

SearchEngine.prototype.process = function (terms) {
    var path = this._settings.url.split('?');
    var query = [this._settings.param, '=', terms].join('');
    var base = path[0], params = path[1], query_string = query;

    if (params) query_string = [params.replace('&amp;', '&'), query].join('&');

    $.get([base, '?', query_string].join(''), $.proxy(function (data) {
        this._settings.result_f(data);
    }, this));
};


SearchEngine.prototype.addTextBox = function (control) {
    control
        .focus()
        .ajaxStart(this.start)
        .ajaxStop(this.stop)
        .keyup($.proxy(function () {
            if (control.val() != this._previousValue) {
                this.resetTimer(this._timer);

                this._timer = setTimeout($.proxy(function () {
                    this.process(control.val())
                }, this), this._settings.delay);

                this._previousValue = control.val();
            }
        }, this));
};
