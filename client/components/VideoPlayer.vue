<template>
  <video
    id="videoplayer"
    controls
    preload="auto"
    ref="videoPlayer"
    class="video-js vjs-big-play-centered"
    @play="onPlayerPlay($event)"
    @pause="onPlayerPause($event)"
    @volumechange="onVolumeChange($event)"
  >
    <audio 
      v-if="audioEnabled"
      :src="audio"
      ref="audioPlayer"
    >
    </audio>
  </video>
</template>

<script>
import videojs from "video.js";
import "videojs-resolution-switcher-webpack";
export default {
  name: "VideoPlayer",

  props: {
    videoData: {
      required: true,
      type: Array
    },
    audio: {
      required: false,
      default: null,
      type: String
    }
  },

  data() {
    return {
      loading: true,  // Determines if the mounted hook is ongoing

      videoPlayer: null,  // Stores VideoJsPlayer

      audioPlayer: null,  // Stores Native HTML audio element (if audio is provided)

      bucketUrl: "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
    };
  },
  mounted() {
    // Initialize the video player
    this.initVideoPlayer();
    
    // Initialize the audio player
    this.initAudioPlayer();

    this.loading = false;
  },
  methods: {
    initVideoPlayer() {
      if (!this.videoData) {
        console.error("videoData not provided so cannot load video player.")
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

      // Save the player to state
      this.videoPlayer = player
    },

    initAudioPlayer() {
      // If the audio is not enabled, do nothing
      if (!this.audioEnabled) {
        return
      }

      // Get the audio player reference
      const player = this.$refs.audioPlayer

      // If the player could not be found, emit error and return
      if (!player) {
        console.error("Could not load audioPlayer ref")
        return
      }

      // Save the audio player to state
      this.audioPlayer = player
    },

    onPlayerPlay(event) {
      // Continue if audio is enabled
      if (!this.audioEnabled) return

      // Get the time stamp from the video
      const time = event.target.currentTime;

      // Sync the time
      this.audioPlayer.currentTime = time

      // Play the audio
      this.audioPlayer.play();
    },
    onPlayerPause(videoPlayer) {
      // Continue if audio is enabled
      if (!this.audioEnabled) return

      // Pause the audio
      this.audioPlayer.pause()
    },
    onVolumeChange(event) {
      // Continue if audio is enabled
      if (!this.audioEnabled) return

      // Get the volume from the video player
      const volume = event.target.volume;

      // Sync the volume
      this.audioPlayer.volume = volume
    }
  },
  computed: {
    audioEnabled() {
      return !!this.audio
    }
  },
  watch: {
    audio() {
      if (this.audioEnabled()) {
        this.initAudioPlayer();
      }
      else {
        this.audioPlayer = null;
      }
    },
    videoData() {
      this.initVideoPlayer()
    }
  }
};
</script>
