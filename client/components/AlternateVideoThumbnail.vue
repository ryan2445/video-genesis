<template>
  <div
    class="thumbnail-blank w-full h-full grid place-content-center"
  >
    <v-icon color="white" large>
      icon-video
    </v-icon>
  </div>
</template>

<script>
export default {
  name: "AlternateVideoThumbnail",
}
</script>

<style scoped>
.thumbnail-blank {
  background: radial-gradient(circle at center, orange 0, black 80%);
}
</style>