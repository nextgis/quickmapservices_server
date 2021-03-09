<template>
  <div class="container py-0">
    <div class="service">
      <div class="btn-group toolbar pull-right" role="group">
        <a href="#" class="btn btn-tool btn--depressed"
          data-toggle="modal"
          data-target=".report-problem-popup"
          :data-service-title="service.name"
          :data-service-id="service.id"
          data-service-url=""
        >Feedback</a>
        <a v-if="isEditingAllowed"
          :href="editUrl"
          class="btn btn-tool btn--depressed"
        >Edit</a>
        <a v-if="isDeletionAllowed" 
          href="#" 
          class="btn btn-tool btn--depressed"
          @click="isDeleteConfirmationShown = true">
          Delete
        </a>
      </div>
      <slot></slot>
      <confirmation-dialog
        v-model = "isDeleteConfirmationShown"
        :btn-true-text="$t('geoservice.deleteConfirmation.btnTrueText')"
        @cancel="isDeleteConfirmationShown = false"
        @confirm="onConfirmDelete()"
      >
        <h4 class="mt-0 mb-2">{{ $t('geoservice.deleteConfirmation.title') }}</h4>
        <div v-html="$t('geoservice.deleteConfirmation.text', { name: service.name})"></div>
      </confirmation-dialog>
    </div>
  </div>
</template>

<script>
import geoserviceService from '@/services/geoserviceService';
import ConfirmationDialog from '@nextgis_common/components/ConfirmationDialog/ConfirmationDialog.vue';

export default {
  name: 'Detail',
  components: { ConfirmationDialog },
  props: {
    isEditingAllowed: {
      type: Boolean,
      default: false
    },
    isDeletionAllowed: {
      type: Boolean,
      default: false
    },
    service: {
      type: Object,
      required: true
    },
    editUrl: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      isDeleteConfirmationShown: false
    }
  },
  methods: {
    onConfirmDelete(){
      this.isDeleteConfirmationShown = false;
      geoserviceService.delete(this.service.guid);
    }
  }
}
</script>

<style>

</style>