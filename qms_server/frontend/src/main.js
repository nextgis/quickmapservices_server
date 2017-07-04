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
import vueConfig from 'vue-config'

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
      "feedback": "Feedback",
      "status_works": "works",
      "status_problematic": "problematic",
      "status_failed": "failed",
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
      "feedback": "Написать автору",
      "status_works": "работает",
      "status_problematic": "есть проблемы",
      "status_failed": "не работает",
    }
  }
})

const configs = {
    apiUrl: {
      geoservices_url: "/api/v1/geoservices/",
      geoservices_type_filter_url: "/api/v1/geoservices/?type={tms|wms|wfs|geojson}",
      geoservices_epsg_filter_url: "/api/v1/geoservices/?epsg={any_epsg_code}",
      geoservices_status_filter_url: "/api/v1/geoservices/?cumulative_status={works|problematic|failed}",
      geoservices_search_url: "/api/v1/geoservices/?search={q}",
      geoservices_intersects_extent_url: "/api/v1/geoservices/?intersects_extent={WKT|EWKT geometry}",
      geoservices_intersects_boundary_url: "/api/v1/geoservices/?intersects_boundary={WKT|EWKT geometry}",
      geoservices_ordering_url: "/api/v1/geoservices/?ordering={name|-name|id|-id|created_at|-created_at|updated_at|-updated_at",
      geoservices_pagination_url: "/api/v1/geoservices/?limit={int}&offset={int}",
      geoservice_detail_url: "/api/v1/geoservices/{id}/",
      geoservice_status_url: "/api/v1/geoservice_status/",
      geoservice_status_detail_url: "/api/v1/geoservice_status/{id}/",
      geoservice_status_service_filter_url: "/api/v1/geoservice_status/?geoservice={id}",
      geoservice_status_cumulative_status_filter_url: "/api/v1/geoservice_status/?cumulative_status={works|problematic|failed}",
      geoservice_status_check_at_ordering_url: "/api/v1/geoservice_status/?ordering={check_at|-check_at}",
      icons_url: "/api/v1/icons/",
      icons_search_url: "/api/v1/icons/?search={q}",
      icons_pagination_url: "/api/v1/icons/?limit={int}&offset={int}",
      icon_detail_url: "/api/v1/icons/{id}/",
      icon_content_url: "/api/v1/icons/{id}/content",
      icon_resized_content_url: "/api/v1/icons/{id}/content?width={16<=x<=64}&height={16<=y<=64}",
      default_icon_url: "/api/v1/icons/default"
  }
}

Vue.use(vueConfig, configs)

/* eslint-disable no-new */
new Vue({
  i18n,
  el: '#app',
  template: '<App/>',
  components: { App }
})
