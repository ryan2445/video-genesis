<template>
  <div>
    <div
      class="grid"
      :class="`grid-${columnLayout ? 'cols' : 'rows'}-${gridColumns}`"
      @contextmenu.prevent="onContextMenu"
    >
      <!-- showStats() {
      this.$emit('show:stats')
      this.$emit('close')
    }, -->
      <video-player
        v-if="previewDefault"
        ref="videoPlayer"
        :audio="audio"
        :start-time="startTime"
        :video-data="videoData"
        :autoplay="autoplay"
        :showStats="showStats"
        @play="handlePlay"
        @pause="handlePause"
        @ended="onEnded"
      />
      <video-preview
        v-if="previewLowRes"
        ref="lowResPlayer"
        :src="`${bucketURL}/${video.videoKey}/${video.lrBaseURL}`"
        hint="DS"
      />
      <video-preview
        v-if="previewHighRes"
        ref="highResPlayer"
        :src="`${bucketURL}/${video.videoKey}/${video.hrBaseURL}`"
        hint="SR"
      />
      <v-menu
        v-model="showContextMenu"
        :position-x="contextMenuX"
        :position-y="contextMenuY"
        transition="v-fade-transition"
        content-class="video-context-menu"
        :close-on-content-click="false"
        outline
      >
        <video-context-menu
          :video="video"
          :videos-shown="gridColumns"
          @close="onContextMenuClose"
          @show:lr="showLowRes"
          @show:hr="showHighRes"
          @show:default="showDefaultPlayer"
          @show:stats="changeStats"
          @sync="onSync"
          @toggle:layout="toggleLayout"
        />
      </v-menu>
    </div>
    <video-player-info :video="video" />
  </div>
</template>

<script>
export default {
  name: "VideoContainer",
  props: {
    video: {
      type: Object,
      required: true,
    },
    audio: {
      type: String,
      required: false,
      default: null,
    },
    startTime: {
      type: String | Number,
      default: null,
      required: false,
    },
    videoData: {
      type: Array,
      required: true,
    },
    autoplay: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      showPreviews: true,
      showContextMenu: false,
      contextMenuX: 0,
      contextMenuY: 0,
      previewDefault: true,
      previewLowRes: false,
      previewHighRes: false,
      showStats: false,
      bucketURL:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      columnLayout: true,
    };
  },
  mounted() {},
  computed: {
    gridColumns() {
      return [
        this.previewDefault,
        this.previewLowRes,
        this.previewHighRes,
      ].reduce((acc, cur) => acc + (cur == true), 0);
    },
  },
  methods: {
    handlePause() {
      const preview1 = this.$refs.lowResPlayer;

      if (preview1)
        preview1.pauseVideo()

      const preview2 = this.$refs.highResPlayer;

      if (preview2)
        preview2.pauseVideo()
    },
    handlePlay() {
      const preview1 = this.$refs.lowResPlayer;

      if (preview1)
        preview1.playVideo()

      const preview2 = this.$refs.highResPlayer;

      if (preview2)
        preview2.playVideo()
    },
    changeStats() {
      this.showStats = !this.showStats;
    },
    onContextMenu(e) {
      this.contextMenuX = e.pageX;
      this.contextMenuY = e.pageY;
      this.showContextMenu = true;
    },
    onContextMenuClose() {
      this.showContextMenu = false;
    },
    showLowRes(bool) {
      this.previewLowRes = bool;
    },
    showHighRes(bool) {
      this.previewHighRes = bool;
    },
    onSync() {
      this.syncLowResVideo()
      this.syncHighResVideo()
    },
    syncLowResVideo() {
      const videoPlayerComponent = this.$refs.videoPlayer;
      const lowResPlayerComponent = this.$refs.lowResPlayer;

      // If the video player does not exist or there are no other players to sync, return
      if (!videoPlayerComponent || !lowResPlayerComponent ) return

      const time = videoPlayerComponent.getCurrentTime();
      const isPaused = videoPlayerComponent.isPaused();

      lowResPlayerComponent.setCurrentTime(time);

      lowResPlayerComponent[isPaused ? 'pauseVideo' : 'playVideo']()
    },
    syncHighResVideo() {
      const videoPlayerComponent = this.$refs.videoPlayer;
      const highResPlayerComponent = this.$refs.highResPlayer;

      // If the video player does not exist or there are no other players to sync, return
      if (!videoPlayerComponent || !highResPlayerComponent ) return

      const time = videoPlayerComponent.getCurrentTime();
      const isPaused = videoPlayerComponent.isPaused();

      highResPlayerComponent.setCurrentTime(time);

      highResPlayerComponent[isPaused ? 'pauseVideo' : 'playVideo']()
    },
    toggleLayout(bool) {
      this.columnLayout = bool;
    },
    showDefaultPlayer(bool) {
      this.previewDefault = bool;
    },
    onEnded() {
      this.$emit("video:ended");
    },
    isPaused() {
      const el = this.$refs.videoPlayer

      if (el) {
        return el.isPaused()
      }

      return true
    }
  },
  watch: {
    previewLowRes(val) {
      if (val) setTimeout(this.syncLowResVideo, 10);
    },
    previewHighRes(val) {
      if (val) setTimeout(this.syncHighResVideo, 10);
    }
  }
};
</script>

<style scoped>
.container-preview {
  display: grid;
  grid-auto-flow: column;
  align-items: center;
}
.prev-1 {
  grid-template-columns: 1fr 1fr;
}
.prev-2 {
  grid-template-columns: 1fr 1fr;
}
.video-context-menu {
  backdrop-filter: blur(8px);
}
</style>
