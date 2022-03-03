<template>
  <div class="relative">
    <video
      id="videoplayer"
      controls
      preload="auto"
      ref="videoPlayer"
      crossorigin="anonymous"
      class="video-js vjs-big-play-centered z-10 w-full h-full"
      @play="onPlayerPlay($event)"
      @pause="onPlayerPause($event)"
      @volumechange="onVolumeChange($event)"
      @resolutionchange="onResChange($event)"
    >
      <audio v-if="audioEnabled" :src="audio" ref="audioPlayer"></audio>
    </video>
  </div>
</template>
<script>
import videojs from "video.js";
import "videojs-resolution-switcher-webpack";
export default {
  props: {
    videoData: {
      required: true,
      type: Array,
    },
    audio: {
      required: false,
      default: null,
      type: String,
    },
  },
  data() {
    return {
      loading: true, // Determines if the mounted hook is ongoing
      videoPlayer: null, // Stores VideoJsPlayer
      audioPlayer: null, // Stores Native HTML audio element (if audio is provided)
      bucketUrl:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      currentVideoSrc: null, // Stores the current src being played
      currentVideoRes: null, // Stores the current resolution of the video
      width: null, // Stores the width of the video element
      height: null, // Stores the height of the video element
      playing: false,
    };
  },
  async mounted() {
    // Initialize the video player
    this.initVideoPlayer();

    // Initialize the audio player
    this.initAudioPlayer();

    this.loading = false;
  },
  methods: {
    initVideoPlayer() {
      if (!this.videoData) {
        console.error("videoData not provided so cannot load video player.");
        return;
      }

      const player = videojs(this.$refs.videoPlayer, {
        fluid: true,
        controls: true,
        sources: this.videoData,
        plugins: {
          videoJsResolutionSwitcher: {
            default: "low",
            dynamicLabel: true,
          },
        },
      });

      // Set the initial height, width of video player
      this.width = this.$refs.videoPlayer.clientWidth;
      this.height = this.$refs.videoPlayer.clientHeight;

      // Create resize observer on video element, tracking its size
      const resizeObserver = new ResizeObserver((entries) => {
        if (!entries || entries.length < 1) {
          console.error("video resize observer with no entries");
          return;
        }

        this.width = entries[0].contentRect.width;
        this.height = entries[0].contentRect.height;
      });

      // Observer the video element
      resizeObserver.observe(this.$refs.videoPlayer);

      // Listen for the resolution change event
      player.on("resolutionchange", this.onResChange);

      // Save the player to state
      this.videoPlayer = player;
    },
    initAudioPlayer() {
      // If the audio is not enabled, do nothing
      if (!this.audioEnabled) {
        return;
      }

      // Get the audio player reference
      const player = this.$refs.audioPlayer;

      // If the player could not be found, emit error and return
      if (!player) {
        console.error("Could not load audioPlayer ref");
        return;
      }

      // Save the audio player to state
      this.audioPlayer = player;
    },
    initCanvasPlayer() {
      if (!this.videoPlayer) {
        console.error(
          "Video player is not initialized. Cannot initialize the canvas player"
        );
        return;
      }

      const canvas = this.$refs.videoCanvas;
      const video = this.$refs.videoPlayer;

      if (!canvas || !video) {
        console.error("Canvas or video ref not found");
        return;
      }

      this.c1 = canvas;
      this.ctx1 = this.c1.getContext("2d");
      this.c_tmp = document.createElement("canvas");
      this.c_tmp.setAttribute("width", this.width);
      this.c_tmp.setAttribute("height", this.height);
      this.ctx_tmp = this.c_tmp.getContext("2d");
    },
    async computeCanvasFrame() {
      const video = this.$refs.videoPlayer;

      this.ctx_tmp.drawImage(video, 0, 0, this.width, this.height);

      let frame = this.ctx_tmp.getImageData(0, 0, this.width, this.height);

      // let processed = this.$tensor.preprocess(frame);

      // const p = this.model.predict(processed);

      // const clip = clipByValue(p.squeeze(), 0, 255).cast('int32')

      // await browser.toPixels(clip, this.c1)

      this.ctx1.putImageData(frame, 0, 0);

      if (this.playing) setTimeout(this.computeCanvasFrame, 0);
    },
    onPlayerPlay(event) {
      // Continue if audio is enabled
      if (!this.audioEnabled) return;

      // Get the time stamp from the video
      const time = event.target.currentTime;

      // Sync the time
      this.audioPlayer.currentTime = time;

      // Play the audio
      this.audioPlayer.play();

      this.playing = true;

      // this.computeCanvasFrame();
    },
    onPlayerPause(videoPlayer) {
      // Continue if audio is enabled
      if (!this.audioEnabled) return;

      // Pause the audio
      this.audioPlayer.pause();
      this.playing = false;
    },
    onVolumeChange(event) {
      console.log(event);
      // Continue if audio is enabled
      if (!this.audioEnabled) return;

      if (event.target.muted) {
        this.audioPlayer.volume = 0;
        return;
      }

      // Get the volume from the video player
      const volume = event.target.volume;

      // Sync the volume
      this.audioPlayer.volume = volume;
    },
    onResChange(event) {
      // Get the current resolution of the video player
      const currentResolution = event.target.player.currentResolution();
      event.target.player.play();

      // Update the video src and res data
      this.setCurrentVideoSrc(currentResolution);
      this.setCurrentVideoRes(currentResolution);
    },
    setCurrentVideoSrc(currentResolution) {
      this.currentVideoSrc = currentResolution.sources[0].src;
    },
    setCurrentVideoRes(currentResolution) {
      this.currentVideoRes = currentResolution.label;
    },
  },
  computed: {
    audioEnabled() {
      return !!this.audio;
    },
  },
  watch: {
    audio() {
      if (this.audioEnabled()) {
        this.initAudioPlayer();
      } else {
        this.audioPlayer = null;
      }
    },
    videoData() {
      this.initVideoPlayer();
    },
  },
};
</script>
