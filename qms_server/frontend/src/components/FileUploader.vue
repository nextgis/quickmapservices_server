<template>
    <div class="file-uploader">
        <bordered-block icon="file_upload"
                        text="<span class='fake-link'>Выберите geoJSON с границами</span> или перетащите его сюда">
            <file-upload v-if = "!disabled"
                :name="name"
                :extensions="extensions"
                :accept="accept"
                :directory="directory"
                :thread="thread"
                :drop="drop"
                :multiple="multiple"
                :dropDirectory="dropDirectory"
                v-model="files"
                @input-file="inputFile"
                ref="upload">
            </file-upload>
            <div v-show="$refs.upload && $refs.upload.dropActive" class="drop-active"></div>
        </bordered-block>
        <div v-if="!files.length" class="file-uploader__help-text caption">
            Файл должен быть в&nbsp;системе координат EPSG:4326В.<br>
            В&nbsp;качестве границы берется геометрия 1-го&nbsp;объекта.
        </div>
        <div v-if="files.length" class="file-uploader__files">
              <div class="file-uploader__file" v-for="(file, index) in files">
                    <!-- <div class="file-uploader__file-image">
                        <img v-if="file.type.substr(0, 6) == 'image/' && file.blob" :src="file.blob"/>
                    </div> -->
                    <div class="file-uploader__file-name">{{file.name}}</div>
                    <div class="file-uploader__file-action">
                        <v-icon class="file-uploader__file-remover" @click="$refs.upload.remove(file)">close</v-icon>
                    </div>
              </div>
        </div>
    </div>
</template>

<script>
import Vue from "vue"
import BorderedBlock from "./BorderedBlock"
import FileUpload from 'vue-upload-component'

export default {
  props: [
    "name",
    "value"
  ],
  components: {
    BorderedBlock,
    FileUpload
  },
  data () {
    return {
        files: [],
        accept: undefined,
        extensions: 'geojson',
        multiple: false,
        directory: false,
        drop: true,
        dropElement: document.querySelector(".drop-active"),
        dropDirectory: false,
        thread: 3,
        auto: false
    }
  },
  watch:{
    value(value){
        if (!value.length) this.files = []
    }
  },
  mounted(){
    this.$forceUpdate()
  },
  methods:{
    inputFile(newFile, oldFile) {
        if (newFile && !oldFile) {
            var URL = window.URL || window.webkitURL
            if (URL && URL.createObjectURL) {
              this.$refs.upload.update(newFile, {blob: URL.createObjectURL(newFile.file)})
            }
        }

        let that = this
        Vue.nextTick(function () {
            that.$emit("fileUploader:changed", that.files)
        })
    }
  }
}
</script>

<style lang="styl">
@require '~vuetify/src/stylus/settings/_colors';

.file-uploader
    width: 100%;
    font-size: 14px;
    
    .bordered-block
        position: relative

    .file-uploads,
    .drop-active
        position: absolute
        width: 100%
        height: 100%
        left: 0
        top:0
        cursor:pointer
        z-index: 2

    .drop-active
        border-radius: 2px
        background-color: rgba(0,112,197, .08)

    &__files
        display: table
        width: 100%
        margin-top: 8px;

    &__file
        display: table-row

        &:hover
            background-color: rgba(0,0,0,.04)


    &__file-image,
    &__file-name,
    &__file-action
        display: table-cell
        vertical-align: middle
        padding: 8px;
    
    &__file-image

        img
            max-height: 60px
            max-width: 150px
            width: auto
            height: auto
            display: block
            border-radius: 4px;
            box-shadow: 0 3px 5px rgba(0,0,0,.16);

    &__file-name
        width: 100%
        border-bottom-left-radius: 4px
        border-top-left-radius: 4px;
        padding-left: 12px;
    
    &__file-action
        text-align: right
        padding-right: 12px;
        border-bottom-right-radius: 4px
        border-top-right-radius: 4px;

    &__file-remover
        cursor: pointer

    &__help-text
        color: $grey.lighten-1
        margin-top: 12px
        line-height: 1.4

</style>
