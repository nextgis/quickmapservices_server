// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'
import App from './App'
import main from '@nextgis_common/js/main'
import './js/search_engine'
import './js/report-problem'
import './js/filter-widget'
import './js/qms'
import './js/preview_map'

main();

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  template: '<App/>',
  components: { App }
})
