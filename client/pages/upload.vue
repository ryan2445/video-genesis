<template>
  <div class="overflow-y-hidden">
    <div class="grid grid-col-1 place-content-center center-upload">
      <video-form />
    </div>
  </div>
</template>
<script>
export default {
  layout: "dashboard",
  created() {
    this.$store.commit("app/setRoute", "Video Upload");
  },
};
</script>
<style scoped>
.center-upload {
  height: calc(100vh - 90px);
}
</style>
