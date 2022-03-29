<template>
  <div class="grid lg:grid-cols-4 md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-x-2 gap-y-3">
    <video-card
      v-for="(video, i) in videos"
      :key="i"
      :video="video"
      :idx="i"
    />
  </div>
</template>

<script>
export default {
  name: "VideoList",
  props: {
    videos: {
      type: Array,
      required: true
    }
  }
};
</script>

<style></style>
