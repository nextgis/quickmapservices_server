export default class SearchEngine {
    constructor(config) {
      this.default_config = {
        url: '/search',
        param: 'query',
        on_success: null,
        delay: 500,
        loading_css: '#loading',
        default_order: 'name',
        search_order: 'name'
      };
      
      this._settings = $.extend(true, this.default_config, config || {});
      this._editBox = null;
      this._filterButtons = [];
      this._activeFilters = {};
    }

   loading() {
      $(this._settings.loading_css).show();
    };

   idle() {
      $(this._settings.loading_css).hide();
    };

   start() {
      $(document).trigger('before.searchbox');
      this.loading();
    };

   stop() {
      this.idle();
      $(document).trigger('after.searchbox')
   };

    resetTimer(timer) {
      if (timer) clearTimeout(timer);
    };

    process() {
      var req_params = $.extend({}, this._activeFilters),
        that = this;
      req_params[this._settings.param] = this._editBox.val();
      if (!this._editBox.val())
        req_params['ordering'] = this._settings.default_order;
      else
        req_params['ordering'] = this._settings.search_order;
      $.get(this._settings.url, req_params, $.proxy(function (data) {
        this._settings.on_success(data).then(function () {
          that.stop();
        });
      }, this));
    };

    addTextBox(control) {
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

    addFilterButton(control, filter_name, filter_val) {
      this._filterButtons.push(control);
      control
        .click($.proxy(function (e) {
          e.preventDefault();

          this._activeFilters = {}; //TODO: single filter!
          this._activeFilters [filter_name] = filter_val; // set value

          $.each(this._filterButtons, function (index, el) {
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
}
