// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue'

import VueI18n from 'vue-i18n'
Vue.use(VueI18n)

import App from './App'

import main from '@nextgis_common/js/main'
import './js/report-problem'
import QmsAddForm from './js/qms'
import './js/preview_map'

main();
var qms = new QmsAddForm()

Vue.config.productionTip = false

const i18n = new VueI18n({
  locale: locale,
  messages: {
    "en": {
      "all_services": "All services",
      "my_services": "My services",
      "last_update": "last update",
      "services_found": "Services found",
      "search_service": "Search map service",
      "no_search_results": "<h2>No results</h2>\
                            Try to change search parameters",
      "edit":"Edit",
      "feedback": "Feedback"
    },
    "ru": {
      "all_services": "Все сервисы",
      "my_services": "Мои сервисы",
      "last_update": "обновлено",
      "services_found": "Найдено сервисов",
      "search_service": "Поиск сервиса",
      "no_search_results": "<h2>Ничего не найдено</h2>\
                            Попробуйте изменить условия поиска",
      "edit":"Редактировать",
      "feedback": "Написать автору"
    }
  }
})

/* eslint-disable no-new */
new Vue({
  i18n,
  el: '#app',
  template: '<App/>',
  components: { App }
})
