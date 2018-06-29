<template>
  <v-app>
    <service-list v-if="isList"></service-list>
  </v-app>  
</template>

<script>

  import Vue from 'vue'
  import Vuetify from 'vuetify'
  import ServiceList from "./components/ServiceList"

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
