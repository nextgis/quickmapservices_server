<template>
  <div>
    <div class="qms__filter row">
        <div class="col-xs-12 col-sm-4 col-sm-push-8">
            <div class="input-group">
                <div class="input-group-addon"><i class="material-icons">search</i></div>
                <div class="form-group">
                    <input v-model="search"
                           @input="updateData(true)"
                           class="form-control" id="txt_search" maxlength="256" :placeholder="$t('search_service')" type="search"
                           style="border-radius:0">
                </div>
            </div>
        </div>
        <div class="col-xs-12 col-sm-8 col-sm-pull-4">
            <service-filter @update="updateFilters"></service-filter>
        </div>
    </div>
    <div class="qms-service-count">
        {{ $t('services_found') }}: <span class="qms-service-count__value">{{data.count}}</span>
    </div>
    <template v-if="data.results && data.results.length > 0">
        <service-card v-for="item in data.results"
                      :service = "item">
        </service-card>
    </template>
    <template v-else>
        <div class="panel panel-default" >
            <div class="panel-body" v-html="$t('no_search_results')">
            </div>
        </div>
    </template>

    <div class="text-xs-center">
      <v-pagination v-if="pageCount>1"
                    :length.number="pageCount"
                    v-model="page"
                    total-visible="10"
                    @input="updateData()"></v-pagination>
    </div>
  </div>
</template>

<script>
  import Vue from 'vue'
  import axios from 'axios'
  import ServiceCard from "./ServiceCard.vue"
  import ServiceFilter from "./ServiceFilter.vue"
  import UrlTemplate from 'url-template'

  export default {
      components:{
        ServiceCard,
        ServiceFilter
      },
      data () {
          return {
              page: 1,
              url: "/api/v1/geoservices/",
              data: {},
              itemsOnPage: 10,
              search: "",
              type: "",
              submitter: ""
          }
      },
      computed: {
         pageCount:function(){
            return this.data ? Math.ceil(this.data.count/this.itemsOnPage) : 0
         },
         ordering: function(){
             return (this.search.length > 0)? "name" : "-updated_at"
         },
         serviceUrlTemplate(){
            return UrlTemplate.parse(this.$config.apiUrl.geoservice_detail_url)
         },
         statusUrlTemplate(){
            return UrlTemplate.parse(this.$config.apiUrl.geoservice_status_detail_url)
         }
      },
      created(){
        this.updateData();
      },
      methods:{
          updateData(resetPage){
              if (resetPage) this.page = 1

              axios.get(this.url, {
                  params: {
                    limit:this.itemsOnPage,
                    offset:(this.page - 1) * this.itemsOnPage,
                    type: this.type,
                    search: this.search,
                    submitter: this.submitter,
                    ordering: this.ordering
                  }
              })
              .then(response => {
                  // JSON responses are automatically parsed.
                  window.scrollTo(0,0)

                  let servicesWithStatus = response.data.results.map((service) => {
                      service.status_text = this.$t('status_' + service.cumulative_status)
                      return service
                  });
                  response.data.results = servicesWithStatus
                  this.data = response.data

                  this.data.results.forEach((service)=>{
                     this.addStatusDescrTo(service)
                  })
              })
              .catch(e => {
                  console.log(e)
              })
          },
          updateFilters(filter){
              this.submitter = ""
              this.type = ""

              this[filter.key] = filter.value
              this.updateData(true)
          },
          addStatusDescrTo(service){
              axios.get(this.serviceUrlTemplate.expand({ id: service.id }))
              .then(response => {
                  let statusId = response.data.last_status

                  axios.get(this.statusUrlTemplate.expand({ id: statusId }))
                  .then(response => {
                      service.status_text = response.data.error_text ? response.data.error_text : this.$t('status_' + response.data.cumulative_status)
                  })
                  .catch(e => {
                      console.log(e)
                  })
              })
              .catch(e => {
                  console.log(e)
              })
          }
      }
  }

</script>
