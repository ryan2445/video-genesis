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

var audio = new Audio();
// this.audiourl
// "https://genesis2vod-staging-outnpm run dveput-q1h5l756.s3.us-west-2.amazonaws.com/3WOzZFlo5ytUFGeUtNWgj/3WOzZFlo5ytUFGeUtNWgj.mp4"

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
    // listen event
    onPlayerPlay(player) {
      // alert(this.src);
      // alert(src);
      audio.play();
    },
    onPlayerPause(player) {
      audio.pause();
      // console.log('player pause!', player)
    },
    // ...player event
    onTimeChange(timeData) {
      console.log("timeData", timeData);
    },

    playerStateChanged(playerCurrentState) {
      alert("123");
      // playerCurrentState.
      console.log("player current update state", playerCurrentState);
    },
    onVideoEnded() {
      audio.currentTime = 0;
    },
    // player is ready
    playerReadied(player) {
      console.log("the player is readied", player);
      // you can use it to do something...
      // player.[methods]
    },
    // player is ready
    onVolumeChange(volumeChange) {
      console.log("the player volume is updated", volumeChange);
      // if this.player.
      audio.volume = this.player.muted() ? 0 : this.player.volume();
      // this.player.
      console.log("current volume is", this.player.volume());
      // you can use it to do something...
      // player.[methods]
    },
    test(dummy) {
      // alert("eventTriggered");
      audio.currentTime = this.player.currentTime();
    },
  },
};
</script>
