<template>
  <div class="qms-list__item panel panel-default" >
      <div class="panel-body">
          <div class="qms-list__item-toolbar btn-group toolbar pull-right" role="group">
              <a :href="url + '?show-report-problem=1'" class="btn btn-tool btn-tool--icon material-icons feedback" :title="$t('feedback')" target="_blank"></a>
              <a v-if="isMy"
                 :href="editUrl" class="btn btn-tool btn-tool--icon material-icons edit" :title="$t('edit')"></a>
          </div>
          <div class="qms-list__title">
              <img class="qms-list__icon" :src="iconUrl+ '?width=24&height=24'" />
              {{ service.name }}
          </div>
          <div v-if="service.desc" class="qms-list__descr">
              {{ service.desc }}
          </div>
          <div class="qms-list__meta">
              <span class="qms-list__meta-item qms-list__type">{{ service.type }}</span>
              <span class="qms-list__meta-item qms-list__date" v-if="service.updated_at">{{ $t('last_update') }}: {{ service.updated_at.slice(0,10) }}</span>
          </div>
      </div>
      <a class="qms-list__link" :href="url" target="_blank"></a>
  </div>
</template>

<script>
    export default {
        props: ["service"],
        data () {
            return {

            }
        },
        computed:{
            url(){
                return "/geoservices/" + this.service.id
            },
            iconUrl(){
                return this.service.icon ? "/api/v1/icons/" + this.service.icon +"/content" : "/api/v1/icons/default"
            },
            editUrl(){
                return "/edit/" + this.service.id
            },
            isMy() {
                return (qmsConfig.user_guid && qmsConfig.user_guid === this.service.submitter)
            }
        }
    }
</script>
