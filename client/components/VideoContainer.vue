<template>
  <div>
    <div
      class="grid"
      :class="`grid-${columnLayout ? 'cols' : 'rows'}-${gridColumns}`"
      @contextmenu.prevent="onContextMenu"
    >
      <video-player
        v-if="previewDefault"
        ref="videoPlayer"
        :audio="audio"
        :start-time="startTime" 
        :video-data="videoData" 
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
          @sync="onSync"
          @toggle:layout="toggleLayout"
        />
      </v-menu>
    </div>
    <video-player-info
      :video="video" 
    />
  </div>
</template>

<script>
export default {
  name: "VideoContainer",
  props: {
    video: {
      type: Object,
      required: true
    },
    audio: {
      type: String,
      required: false,
      default: null
    },
    startTime: {
      type: String | Number,
      default: null,
      required: false
    },
    videoData: {
      type: Array,
      required: true
    }
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
      bucketURL: "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      columnLayout: true
    }
  },
  mounted() {

  },
  computed: {
    gridColumns() {
      return [this.previewDefault, this.previewLowRes, this.previewHighRes].reduce((acc, cur) => acc + (cur == true), 0)
    }
  },
  methods: {
    onContextMenu(e) {
      this.contextMenuX = e.pageX
      this.contextMenuY = e.pageY
      this.showContextMenu = true
    },
    onContextMenuClose() {
      this.showContextMenu = false
    },
    showLowRes(bool) {
      this.previewLowRes = bool
    },
    showHighRes(bool) {
      this.previewHighRes = bool
    },
    onSync() {
      const videoPlayerComponent = this.$refs.videoPlayer;
      const lowResPlayerComponent = this.$refs.lowResPlayer;
      const highResPlayerComponent = this.$refs.highResPlayer;

      // If the video player does not exist or there are no other players to sync, return
      if (!videoPlayerComponent || (!lowResPlayerComponent && !highResPlayerComponent)) {
        return
      }

      const time = videoPlayerComponent.getCurrentTime()
      const isPaused = videoPlayerComponent.isPaused()

      if (!!lowResPlayerComponent) {
        lowResPlayerComponent.setCurrentTime(time)

        if (isPaused) {
          lowResPlayerComponent.pauseVideo()
        }
        else {
          lowResPlayerComponent.playVideo()
        }
      }
      if (!!highResPlayerComponent) {
        highResPlayerComponent.setCurrentTime(time)

        if (isPaused) {
          highResPlayerComponent.pauseVideo()
        }
        else {
          highResPlayerComponent.playVideo()
        }
      }
    },
    toggleLayout(bool) {
      this.columnLayout = bool
    },
    showDefaultPlayer(bool) {
      this.previewDefault = bool
    }
  }
  
}
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
</style>
