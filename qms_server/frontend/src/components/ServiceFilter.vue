<template>
    <ul class="qms__filter__list filter-links list-inline">
        <li class="filter-links__item" v-for="filter in filters">
            <a :class="['filter-link', { 'active' : filter.active }]"
               @click.stop = "activateFilter(filter)"
               href="#">
                <span class="filter-link__inner">{{ filter.text }}</span>
            </a>
        </li>
    </ul>
</template>

<script>
    export default {
        data () {
            return {
                filters: [
                  {
                      key: 'type',
                      value: "",
                      text: this.$t('all_services'),
                      active: true
                  },
                  {
                      key: 'type',
                      value: "tms",
                      text: "TMS",
                      active: false
                  },
                  {
                      key: 'type',
                      value: "wms",
                      text: "WMS",
                      active: false
                  },
                  {
                      key: 'type',
                      value: "wfs",
                      text: "WFS",
                      active: false
                  },
                  {
                      key: 'type',
                      value: "geojson",
                      text: "GeoJSON",
                      active: false
                  }
                ]
            }
        },
        methods:{
            activateFilter(filter){
                this.filters.forEach(function(item, i, arr) {
                    if (item === filter){
                        item.active = true
                    } else {
                        item.active = false
                    }
                });
                this.$emit('update', filter)
            }
        },
        created(){
            if (qmsConfig.user_guid){
                this.filters.push({
                    key: 'submitter',
                    value: qmsConfig.user_guid,
                    text: this.$t('my_services'),
                    active: false
                })
            }
        }
    }
</script>
