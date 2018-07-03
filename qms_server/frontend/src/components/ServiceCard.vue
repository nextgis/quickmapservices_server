<template>
  <div class="service-card service-card panel panel-default" >
      <div class="panel-body">
          <div v-if="service.cumulative_status"
               :class="['service-card__status', statusClass]"
               :title="service.status_text"></div>
          <div class="service-card__toolbar icon-toolbar icon-toolbar--v icon-toolbar--s">
            <v-btn icon class="icon-toolbar__btn grey--text text--lighten-1"
                        tag="a"
                        v-if="isMy"
                        :href="editUrl"
                        :title="$t('edit')">
              <v-icon>edit</v-icon>
            </v-btn>
            <v-btn icon class="icon-toolbar__btn grey--text text--lighten-1"
                        tag="a"
                        :href="url + '?show-report-problem=1'"
                        :title="$t('feedback')">
              <v-icon>feedback</v-icon>
            </v-btn>
          </div>
          <div class="service-card__title">
              <img class="service-card__icon" :src="iconUrl+ '?width=24&height=24'" />
              {{ service.name }}
          </div>
          <div v-if="service.desc" class="service-card__descr">
              {{ service.desc }}
          </div>
          <div class="service-card__meta">
              <span class="service-card__meta-item service-card__type">{{ service.type }}</span>
              <span class="service-card__meta-item service-card__date" v-if="service.updated_at">{{ $t('last_update') }}: {{ service.updated_at.slice(0,10) }}</span>
          </div>
      </div>
      <a class="service-card__link" :href="url" target="_blank"></a>
  </div>
</template>

<script>
    import Vue from 'vue'
    import axios from 'axios'

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
            },
            statusClass() {
                switch (this.service.cumulative_status) {
                  case 'works':
                    return 'success';
                    break;
                  case 'failed':
                    return 'error';
                    break;
                  case 'problematic':
                    return 'warning';
                    break;
                }
            }
        }
    }
</script>


<style lang="styl">
  @require '~vuetify/src/stylus/settings/_colors';
  @require '~@nextgis_common/scss/custom-vuetify/_theme'
  @require '~@nextgis_common/scss/custom-vuetify/_variables'

  .service-card
      position: relative;
      transition: box-shadow .3s;
      width: 100%;
      min-height: 100px;

      &:hover
          box-shadow: 0 8px 10px 1px rgba(0, 0, 0, .07),
                      0  3px 14px 2px rgba(0, 0, 0, .1),
                      0  5px 5px -3px rgba(0, 0, 0, .06); // @include  shadow-8dp

          .service-card__toolbar
              opacity: 1;


          .service-card__title
              color: $theme.primary;

  .service-card__link
      position: absolute;
      left:0;
      top:0;
      width: 100%;
      height: 100%;
      z-index: 2;
      border-bottom: 0;

  .service-card__meta
      color: #888;
      font-size: 13px;
      margin-top: 16px;
      margin-bottom: -6px;

      .service-card__meta-item
          position: relative;
          margin-left: 24px;

          &::before
              content:"";
              position: absolute;
              left: -16px;
              top: 6px;
              width: 5px;
              height: 5px;
              background-color: #c9dced;
              border-radius: 50%;

          &:first-child
              margin-left:0;

              &::before
                  display: none;

      .service-card__type
          text-transform: uppercase;

  .service-card__title
      font-size: 19px;
      padding-left: 34px;
      padding-right: 80px;
      margin-bottom: 8px;
      font-weight: bold;

      .service-card__icon
          float:left;
          margin-left: -34px;
          margin-top: 1px;

  .service-card__toolbar
      position: absolute;
      right: 4px;
      bottom: 4px;
      z-index: 10;
      opacity:0;

  .service-card__status
      position: absolute;
      top: 14px;
      right: 14px;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background-color: $theme.primary;
      z-index: 10;

  .icon-toolbar
    &--v
      .icon-toolbar__btn
        display: flex;
        margin:0;

        &:hover
          &:before
            background-color: transparent

          .v-icon
            color: $theme.primary  

    &--s
      .icon-toolbar__btn
        width: 32px;
        height: 32px;

        .v-icon
          font-size: 22px;

</style>
