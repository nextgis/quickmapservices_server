<template>
  <service-list v-if="isList"></service-list>
</template>

<script>

  import Vue from 'vue'
  import Vuetify from 'vuetify'
  import ServiceList from "./components/ServiceList"

  Vue.use(Vuetify)


  export default {
    name: 'app',
    components:{
        ServiceList
    },
    data () {
        return{
           isList: ($("#app").length>0)
        }
    }
  }

</script>

<style lang="scss">
  @import "~@nextgis_common/scss/main";
  @import "./scss/qms";
</style>

<style lang="styl">
  @import "~@nextgis_common/scss/vuetify"
</style>
