<template>
  <v-menu
    v-model="showUploadVideoForm"
    offset-y
    left
    nudge-bottom="2"
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-hover v-slot="{ hover }">
        <v-btn
          style="right: 0%; margin-right: 8px"
          absolute
          v-bind="attrs"
          v-on="on"
          dense
          height="30"
          color="#A13440"
          :style="{ 'background-color': hover ? '#c64050' : '#A13440' }"
        >
          <div class="text-white">
            <v-icon class="mr-2"> mdi-cloud-upload </v-icon>
            Upload Video
          </div>
        </v-btn></v-hover
      >
    </template>
    <upload-video-form @close="showUploadVideoForm = false" />
  </v-menu>
</template>

<script>
export default {
  name: "UploadVideoButton",
  data() {
    return {
      showUploadVideoForm: false,
    };
  },
};
</script>
<style scoped></style>
