<template>
  <v-menu
    v-model="showUploadVideoForm"
    offset-y nudge-left="435" 
    nudge-bottom="2" 
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        absolute
        class="top-1 right-3 z-10"
        v-bind="attrs"
        v-on="on"
        dense
        height="30"
      >
        <span class="text-app-orange">
          Upload Video
        </span>
      </v-btn>
    </template>
    <upload-video-form @close="showUploadVideoForm = false" />
  </v-menu>
</template>

<script>
export default {
  name: "UploadVideoButton",
  data() {
    return {
      showUploadVideoForm: false
    }
  }
}
</script>