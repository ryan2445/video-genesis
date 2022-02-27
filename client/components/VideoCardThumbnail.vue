<template>
  <VueVideoThumbnail
    :style="{
      opacity: thumbnailReady ? '1' : '0'
    }"
    :video-src="getLink(video)"
    :snapshot-at-duration-percent="70"
    :width="380"
    @snapshotCreated="onSnapshotCreated"
  >
    <template #snapshot="{ snapshot }">
      <img
        v-if="snapshot"
        :src="video.videoThumbnail || snapshot"
        alt="snapshot"
        :width="380"
        :height="280"
        style="object-fit:contain; min-width:380px; min-height:280px; max-width:380px; max-height:280px;"
      />
    </template>
  </VueVideoThumbnail>
</template>

<script>
export default {
  name: "VideoCardThumbnail",
  props: {
    video: {
      type: Object,
      required: true
    }
  },
  computed: {
    
  }
}
</script>