<template>
  <div class="grid grid-col-1 place-content-center h-screen overflow-y-hidden">
    <video-form />
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
<style scoped></style>
