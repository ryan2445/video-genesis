<template>
  <div
    class="relative flex flex-1"
  >
      <div
        v-if="!!hint"
        class="absolute top-4 right-4 preview-title"
      >
        <span
          class="text-gray-100"
        >
          {{ hint }}
        </span>
      </div>
      <video 
        ref="videoPlayer"
        muted
      >
        <source 
          :src="src" 
          type="video/mp4"
        >
      </video>
  </div>
</template>

<script>
export default {
  name: "VideoPreview",
  props: {
    src: {
      type: String,
      required: false
    },
    hint: {
      type: String,
      required: false
    }
  },
  methods: {
    setCurrentTime(time) {
      const el = this.$refs.videoPlayer

      if (!el) return

      el.currentTime = time
    },
    playVideo() {
      const el = this.$refs.videoPlayer

      if (!el) return

      el.play()
    },
    pauseVideo() {
      const el = this.$refs.videoPlayer

      if (!el) return

      el.pause()
    }
  }
}
</script>

<style scoped>
.preview-title {
  padding: 2px 3px;
  background: rgba(41, 40, 40, 0.5);
  backdrop-filter: blur(6px);
}
</style>