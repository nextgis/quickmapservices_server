<template>
  <div>
    <div class="qms__filter row">
      <div class="col-xs-12 col-sm-4 col-sm-push-8">
        <div class="input-group">
          <div class="input-group-addon">
            <i class="material-icons">search</i>
          </div>
          <div class="form-group">
            <input
              v-model="search"
              @input="updateData(true)"
              class="form-control"
              id="txt_search"
              maxlength="256"
              :placeholder="$t('search_service')"
              type="search"
              style="border-radius:0"
            >
          </div>
        </div>
      </div>
      <div class="col-xs-12 col-sm-8 col-sm-pull-4">
        <service-filter @update="updateFilters"></service-filter>
      </div>
    </div>
    <div class="qms-service-count">
      {{ $t('services_found') }}:
      <span class="qms-service-count__value">{{data.count}}</span>
    </div>
    <template v-if="data.results && data.results.length > 0">
      <service-card v-for="item in data.results" v-bind:key="item.id" :service="item"></service-card>
    </template>
    <template v-else>
      <div class="panel panel-default">
        <div class="panel-body" v-html="$t('no_search_results')"></div>
      </div>
    </template>
    <v-pagination
      v-if="pageCount > 1"
      :length = "pageCount"
      v-model = "page"
      total-visible="10"
      @input="updateData()"
    ></v-pagination>
  </div>
</template>

<script>
import Vue from "vue";
import ServiceCard from "./ServiceCard.vue";
import ServiceFilter from "./ServiceFilter.vue";
import UrlTemplate from "url-template";

export default {
  components: {
    ServiceCard,
    ServiceFilter
  },
  data() {
    return {
      page: 1,
      url: "/api/v1/geoservices/",
      data: {},
      itemsOnPage: 10,
      search: "",
      type: "",
      submitter: ""
    };
  },
  computed: {
    pageCount: function() {
      return this.data ? Math.ceil(this.data.count / this.itemsOnPage) : 0;
    },
    ordering: function() {
      return this.search.length > 0 ? "name" : "-updated_at";
    },
    serviceUrlTemplate() {
      return UrlTemplate.parse(this.$config.apiUrl.geoservice_detail_url);
    },
    statusUrlTemplate() {
      return UrlTemplate.parse(
        this.$config.apiUrl.geoservice_status_detail_url
      );
    }
  },
  created() {
    this.updateData();
  },
  methods: {
    updateData(resetPage) {
      if (resetPage) this.page = 1;

      const url = new URL(this.url, location.origin);
      const params = {
        limit: this.itemsOnPage,
        offset: (this.page - 1) * this.itemsOnPage,
        type: this.type,
        search: this.search,
        submitter: this.submitter,
        ordering: this.ordering
      };
      url.search = new URLSearchParams(params);
      fetch(url)
        .then(resp => resp.json())
        .then(json => {
          // JSON responses are automatically parsed.
          window.scrollTo(0, 0);

          let servicesWithStatus = json.results.map(service => {
            service.status_text = this.$t(
              "status_" + service.cumulative_status
            );
            return service;
          });
          json.results = servicesWithStatus;
          this.data = json;
        })
        .catch(e => {
          console.log(e);
        });
    },
    updateFilters(filter) {
      this.submitter = "";
      this.type = "";

      this[filter.key] = filter.value;
      this.updateData(true);
    }
  }
};
</script>
