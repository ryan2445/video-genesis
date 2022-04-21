<template>
  <div class="relative">
    <div v-if="showStats" class="absolute z-10 bg-black bg-opacity-75 m-2">
      <div class="p-2 grid grid-cols-2 gap-x-2">
        <div v-for="stat in videoStats" :key="stat.title" class="flex flex-row">
          <div class="text text-xs">
            <span class="text-white font-bold">
              {{ stat.title }}:&nbsp 
            </span>
          </div>
          <div class="text-xs">
            <span class="text-white">
              {{ stat.value }}
            </span>
          </div>
        </div>
      </div>
    </div>
    <video
      v-if="!autoplay"
      id="videoplayer"
      controls
      preload="auto"
      ref="videoPlayer"
      class="video-js vjs-big-play-centered vjs-16-9"
      @play="onPlayerPlay($event)"
      @pause="onPlayerPause($event)"
      @volumechange="onVolumeChange($event)"
      @resolutionchange="onResChange($event)"
      @ended="onEnded($event)"
    >
      <audio v-if="audioEnabled" :src="audio" ref="audioPlayer"></audio>
    </video>
    <video
      v-else-if="autoplay"
      id="videoplayer"
      controls
      autoplay
      preload="auto"
      ref="videoPlayer"
      class="video-js vjs-big-play-centered vjs-16-9"
      @play="onPlayerPlay($event)"
      @pause="onPlayerPause($event)"
      @volumechange="onVolumeChange($event)"
      @resolutionchange="onResChange($event)"
      @ended="onEnded($event)"
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
    startTime: {
      required: false,
      default: null,
      type: String | Number,
    },
    autoplay: {
      type: Boolean,
      required: false,
      default: false,
    },
    showStats: { type: Boolean },
    video: {
      type: Object,
      required: false,
      default: null
    }
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
        fluid: false,
        controls: true,
        sources: this.videoData,
        responsive: false,
        aspectRatio: "16:9",
        autoplay: this.autoplay,
        fill: true,
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

      // Update the start time
      if (this.startTime != null) {
        this.$refs.videoPlayer.currentTime =
          typeof this.startTime == "string"
            ? Number(this.startTime)
            : this.startTime;
      }
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
    onPlayerPlay(event) {
      this.$emit("play");

      // Continue if audio is enabled
      if (!this.audioEnabled) return;

      // Get the time stamp from the video
      const time = event.target.currentTime;

      // Sync the time
      this.audioPlayer.currentTime = time;

      // Play the audio
      this.audioPlayer.play();

      this.playing = true;
    },
    onPlayerPause(videoPlayer) {
      this.$emit("pause");

      // Continue if audio is enabled
      if (!this.audioEnabled) return;

      // Pause the audio
      this.audioPlayer.pause();

      this.playing = false;
    },
    onVolumeChange(event) {
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
    getCurrentTime() {
      return this.$refs.videoPlayer?.currentTime;
    },
    isPaused() {
      const el = this.$refs.videoPlayer;
      if (!el) return true;
      return this.$refs.videoPlayer.paused;
    },
    onEnded() {
      this.$emit("ended");
    },
    updateVideoSource() {
      if (!this.videoPlayer) return

      this.videoPlayer.updateSrc(this.videoData)
    }
  },
  computed: {
    audioEnabled() {
      return !!this.audio;
    },
    videoStats() {
      if (!this.videoPlayer) return

      const stats = [
        {
          title: "Aspect Ratio",
          value: this.videoPlayer.aspectRatio_
        },
        {
          title: "Height",
          value: this.videoPlayer.tech_.el_.videoHeight
        },
        {
          title: "Width",
          value: this.videoPlayer.tech_.el_.videoWidth
        },
        {
          title: "Duration",
          value: this.videoPlayer.tech_.el_.duration
        },
        {
          title: "Audio",
          value: this.videoPlayer.isAudio_
        },
        {
          title: "Type",
          value: this.videoPlayer.cache_.source.type
        },
        {
          title: "Elapsed Time",
          value: this.videoPlayer.cache_.currentTime
        }
      ]

      if (this.video) {
        const data = this.video.videoData.find(d => d.width == this.currentVideoRes )
        if (data) {
          stats.push(...[{
            title: "Codec",
            value: data.codecs
          }, {
            title: "Scan Type",
            value: data.scanType
          }, {
            title: "Base URL",
            value: data.baseURL
          }])
        }
      }

      return stats
    }
  },
  watch: {
    audio() {
      if (this.audioEnabled) {
        this.initAudioPlayer();
      } else {
        this.audioPlayer = null;
      }
    },
    videoData() {
      this.updateVideoSource();
    },
    autoplay() {
      this.initVideoPlayer();
    },
  },
};
</script>
