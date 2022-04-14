<template>
  <div
    class="thumbnail-blank w-full h-full grid place-content-center"
  >
    <div class="flex flex-col">
      <v-icon color="white" large>
        icon-video
      </v-icon>
      <div v-if="!processed">
        <p class="text-white">processing...</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "AlternateVideoThumbnail",
  props: {
    processed: {
      default: true,
      required: false,
      type: Boolean
    }
  }
}
</script>

<style scoped>
.thumbnail-blank {
  background: radial-gradient(circle at center, orange 0, black 80%);
}
</style>