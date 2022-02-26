<template>
  <div class="grid place-items-center h-screen">
    <video-form />
  </div>
</template>

<script>
import UploadBox from "../components/UploadBox.vue";
export default {
  components: { UploadBox },
  layout: "dashboard",
  created() {
    this.$store.commit("app/setRoute", "Video Upload");
  },
};
</script>

<style scoped></style>
