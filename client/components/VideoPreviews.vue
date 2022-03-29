<template>
  <div class="grid grid-cols-2 gap-0">
    <video-preview 
      :src="`${bucketURL}/${video.videoKey}/${video.lrBaseURL}`"
      hint="DS"
    />
    <video-preview
      :src="`${bucketURL}/${video.videoKey}/${video.hrBaseURL}`"
      hint="SR"
    />
  </div>
</template>

<script>
export default {
  name: "VideoPreviews",
  props: {
    video: {
      type: Object,
      required: true
    },
    showHR: {
      type: Boolean,
      required: false,
      default: false
    },
    showLR: {
      type: Boolean,
      required: false,
      default: false
    }
  },
  data() {
    return {
      bucketURL: "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com"
    }
  },
  methods: {
    onError(err) {
      console.log('err')
      console.log(err)
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