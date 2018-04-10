<template>
    <div class="file-uploader">
        <label class="file-uploader__label" :class="{'error--text':error}">{{ label }}</label>
        <div v-if="filename" class="file-uploader__file"> 
            <template v-if="filelink">
                <a :href="filelink">{{ filename }}</a>
            </template>
            <template v-else>
                {{ filename }}
            </template>
        </div>
        <div class="file-uploader__actions">                
            <a href="#" class="btn btn-tool file-uploader__action"
                    @click="onClick">{{ uploadLabel }}</a>
            <a href="#" v-if="filename" class="file-uploader__action secondary-link"
                        @click="removeFile">{{ removeLabel }}</a>
        </div>
        <div v-if="hint && !error" class="file-uploader__hint">{{ hint }} </div>
        <div v-if="error" class="file-uploader__hint error--text">{{ errorMessageComputed }}</div>
        <input type="file" :accept="accept" :multiple="false" :disabled="disabled" :name="name"
               ref="fileInput" @change="onFileChange">
        <input class="hidden" type="checkbox" name="boundary_remove" :checked="fileRemoved">
    </div>
</template>
<script>
    export default{
        props: {
            name: {
                type: "String"
            },
            valueName: {
                type: [String, Array]
            },
            valueLink:{
                type: String
            },
            accept: {
                type: String,
                default: "*"
            },
            label: {
                type: String,
                default: "Please choose..."
            },
            uploadLabel: {
                type: String,
                default: "Upload file..."
            },
            removeLabel: {
                type: String,
                default: "Delete"
            },
            required: {
                type: Boolean,
                default: false
            },
            disabled: {
                type: Boolean,
                default: false
            },
            multiple: {
                type: Boolean, // not yet possible because of data
                default: false
            },
            hint: {
                type: String
            },
            errorMessage:{
                type: String
            },
            removeConfirmText:{
                type: String            }
        },
        data(){
            return {
                filename: "",
                filelink: undefined,
                fileRemoved: false
            };
        },
        watch: {
            valueName(v){
                this.filename = v;
            },
            valueLink(v){
                this.filelink = v;
            }
        },
        computed:{
            error(){
                return this.errorMessage.length>0
            },
            errorMessageComputed(){
                return this.error ? this.errorMessage.substring(2) : ""
            }
        },
        mounted() {
            this.filename = this.valueName;
            this.filelink = this.valueLink;
        },
        methods: {
            getFormData(files){
                const data = new FormData();
                [...files].forEach(file => {
                    data.append('data', file, file.name); // currently only one file at a time
                });
                return data;
            },
            onClick(){
                if (!this.disabled) {
                    debugger;
                    this.$refs.fileInput.click();
                }
            },
            removeFile(){
                if (confirm(this.removeConfirmText)){
                    this.$refs.fileInput.value = null;
                    this.filename = null;
                    this.fileRemoved = true;
                    this.onFileChange();
                }
            },
            onFileChange($event){
                const files = $event ? $event.target.files || $event.dataTransfer.files : [];
                const form = this.getFormData(files);
                if (files) {
                    if (files.length > 0) {
                        this.filename = [...files].map(file => file.name).join(', ');
                        this.filelink = null;
                        this.fileRemoved = false;
                    } else {
                        this.filename = null;
                    }
                } else {
                    this.filename = $event.target.value.split('\\').pop();
                }
                this.errorMessage = "";
                this.$emit('input', this.filename);
                this.$emit('formData', form);
            }
        }
    };
</script>

<style lang="scss" scoped>
    @import '~@nextgis_common/scss/variables/_bootstrap_variables';

    input[type=file]{
        position: absolute;
        left: -99999px;
    }    

    .file-uploader{

        &__actions{
            font-size: 14px;
            font-family: $headings-font-family;
        }    

        &__action{
            display: inline-block;
            vertical-align: middle;
            margin-right: 12px;
            margin-top:0;
        }

        &__file{
            margin-bottom: 8px;
        }

        &__hint{
            font-size: 12px;
            margin-top: 12px;
            color: rgba(0,0,0,.48);
        }

        &__label{
            margin-bottom: 12px;
        }
    }

</style>