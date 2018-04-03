<template>
    <div class="bordered-block">
        <v-icon large class="bordered-block__icon">{{ icon }}</v-icon>
        <div class="bordered-block__text" v-html="text"></div>
        <slot></slot>
    </div>
</template>

<script>
    export default {
      props: [
        "icon",
        "text"
      ]
    }
</script>

<style lang="styl">

@require '~vuetify/src/stylus/settings/_colors';


.bordered-block
    width: 100%
    height: 85px
    display: flex
    flex-direction: row
    align-items: center
    justify-content: flex-start
    border: 1px dashed $grey.base
    border-radius:2px


    &__icon
        width: 80px;
        text-align:center;
</style>
