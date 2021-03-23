// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.

import Vue from 'vue';

import VueI18n from 'vue-i18n';
Vue.use(VueI18n);

import Vuetify from 'vuetify';
import ServiceList from "./components/ServiceList";
import ServiceDetail from "./components/ServiceDetail";

import '@nextgis_common/js/ngkit-components';
import main from '@nextgis_common/js/main';
import './js/report-problem';
import QmsAddForm from './js/qms';
import './js/preview_map';
import vueConfig from 'vue-config';


import SidebarMenu from '@nextgis_common/components/SidebarMenu/SidebarMenu.vue';
import SelfLink from '@nextgis_common/components/SelfLink/SelfLink.vue';

//styles
import "@nextgis_common/scss/main.scss";
import "@nextgis_common/scss/vuetify.styl";
import './scss/qms.scss';

Vue.use(Vuetify, { 
    theme: {
        primary: '#0070c5',
        accent: '#00b77e',
        secondary: '#e5eef7',
        info: '#2196f3',
        warning: '#ffc107',
        error: '#ff5252',
        success: '#4caf50'
    }   
});

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
      "delete": "Delete",
      "status_works": "works",
      "status_problematic": "problematic",
      "status_failed": "failed",
      "geoservice": {
        "deleteConfirmation": {
          "title": "Delete this service?",
          "text": "Are you about to delete <strong>{name}</strong>. This&nbsp;is&nbsp;not&nbsp;recoverable.",
          "btnTrueText": "Delete",
        }
      }
    },
    "ru": {
      "all_services": "Все сервисы",
      "my_services": "Мои сервисы",
      "last_update": "обновлено",
      "services_found": "Найдено сервисов",
      "search_service": "Поиск сервиса",
      "no_search_results": "<h2>Ничего не найдено</h2>\
                            Попробуйте изменить условия поиска",
      "edit":"Изменить",
      "feedback": "Написать автору",
      "delete": "Удалить",
      "status_works": "работает",
      "status_problematic": "есть проблемы",
      "status_failed": "не работает",
      "geoservice": {
        "deleteConfirmation": {
          "title": "Удалить сервис?",
          "text": "Вы собираетесь удалить <strong>{name}</strong>. Это&nbsp;действие нельзя отменить.",
          "btnTrueText": "Удалить",
        }
      }
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

new Vue({
  i18n,
  el: '#app',
  components: { ServiceList, SelfLink, SidebarMenu, ServiceDetail },
  data() {
    return {
      sidebarMenuShown: false
    }
  }
})

main();

var qms = new QmsAddForm()