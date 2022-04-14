<template>
  <v-menu
    v-model="showUploadVideoForm"
    offset-y left nudge-bottom="2" 
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn style="right:0%; margin-right:8px;"
        absolute
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
