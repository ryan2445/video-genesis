<template>
  <div class="flex flex-col justify-center bg-gray-200 px-10 py-4 relative">
    <v-progress-linear absolute top indeterminate rounded :active="uploading" />
    <div>
      <v-file-input
        id="video-file-upload-input"
        label="Upload video"
        @change="onFileInputChange"
        show-size
        :loading="uploading"
        filled
        color="#A13440"
        prepend-icon=""
        prepend-inner-icon="mdi-file-video"
        accept="video/mp4"
      >
      </v-file-input>
    </div>
  </div>
</template>
<script>
export default {
  layout: "dashboard",
  data() {
    return {
      video: null,

      uploading: false,
    };
  },
  mounted() {},
  methods: {
    onFileInputChange(file) {
      this.video = file;

      this.$emit("update", file);
    },
    resetUploadBox() {
      this.video = null;
    },
  },
};
</script>
