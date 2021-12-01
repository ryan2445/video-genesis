<template>
  <div>
    <video
      controls
      preload="auto"
      ref="videoPlayer"
      class="video-js vjs-big-play-centered"
    >
      <source :src="src" type="" />
    </video>
    <video-player-info />
  </div>
</template>

<script>
import videojs from "video.js";
import "video.js/dist/video-js.min.css";
import VideoPlayerInfo from "./VideoPlayerInfo.vue";

export default {
  components: { VideoPlayerInfo },
  name: "VideoPlayer",

  props: ["src"],

  data() {
    return {
      player: null,
    };
  },
  mounted() {
    this.player = videojs(this.$refs.videoPlayer, { fluid: true });
  },
};
</script>
