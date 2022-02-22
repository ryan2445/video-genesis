<template>
  <div>
    <video
      id="videoplayer"
      controls
      preload="auto"
      ref="videoPlayer"
      class="video-js vjs-big-play-centered"
      @play="onPlayerPlay($event)"
      @pause="onPlayerPause($event)"
      @statechanged="playerStateChanged($event)"
      @volumechange="onVolumeChange($event)"
      @seeked="test($event)"
      @ended="onVideoEnded()"
    >
      <!-- @timeupdate="onTimeChange($event)" -->
    </video>
  </div>
</template>

<script>
import videojs from "video.js";
import "video.js/dist/video-js.min.css";
import "videojs-resolution-switcher-webpack";

let audio = new Audio();

export default {
  name: "VideoPlayer",

  props: ["src", "audiourl", "video"],

  data() {
    return {
      loading: true,
      player: null,
      bucketUrl:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
    };
  },
  mounted() {
    var sources = [];
    var videoInfos = JSON.parse(this.video.videoData);
    Array.from(videoInfos).forEach((vinfo) =>
      sources.push({
        type: "video/mp4",
        src: `${this.bucketUrl}/${this.video.videoKey}/${vinfo.baseURL}`,
        label: `${vinfo.width}`,
        res: vinfo.width,
      })
    );
    console.log("thse are the sources", sources);

    this.player = videojs(this.$refs.videoPlayer, {
      fluid: true,
      controls: true,
      sources: sources,
      plugins: {
        videoJsResolutionSwitcher: {
          default: "low",
          dynamicLabel: true,
        },
      },
    });
    audio = new Audio(this.audiourl);
    this.loading = false;
  },
  methods: {
    onPlayerPlay(player) {
      audio.play();
    },
    onPlayerPause(player) {
      audio.pause();
    },

    onTimeChange(timeData) {
      console.log("timeData", timeData);
    },

    playerStateChanged(playerCurrentState) {
      alert("123");

      console.log("player current update state", playerCurrentState);
    },
    onVideoEnded() {
      audio.currentTime = 0;
    },

    playerReadied(player) {
      console.log("the player is readied", player);
    },

    onVolumeChange(volumeChange) {
      console.log("the player volume is updated", volumeChange);

      audio.volume = this.player.muted() ? 0 : this.player.volume();

      console.log("current volume is", this.player.volume());
    },
    test(cur_time) {
      audio.currentTime = this.player.currentTime();
    },
  },
};
</script>
