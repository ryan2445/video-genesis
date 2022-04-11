<template>
  <v-tooltip bottom open-delay="500">
    <template
      v-slot:activator="{ on, attrs }"
    >
      <v-btn
        icon
        v-bind="attrs"
        v-on="on"
        @click="handleClick"
        :color="buttonColor"
      >
        <v-icon>
          icon-lightning-bolt-circle
        </v-icon>
      </v-btn>
    </template>
    <span>
      {{ tooltipText }}
    </span>
  </v-tooltip>
</template>

<script>
export default {
  name: "VideoSuperResolution",
  props: {
    video: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      BUCKET_URL: 'https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com'
    }
  },
  mounted() {
    this.$store.dispatch('sr/checkServer')
  },
  methods: {
    handleClick() {
      if (!this.serverRunning) {
        this.$notify({
          text: 'The SR server is not running. Please check back later'
        })
      }
      else if (this.processedState == 1) {
        this.$notify({
          text: 'The video is currently being processed, check back later'
        });
      }
      else if (this.processedState == 2) {
        this.$notify({
          text: 'This video has been processed with super resolution. Right click on the video for more info'
        });
      }
      else this.processVideo()
    },
    async processVideo() {
      const params = {
        video_key: this.video.videoKey,
        video_url: `${this.BUCKET_URL}/${this.video.videoKey}/${this.video.videoKey}_3000.mp4`
      }

      const response = await this.$store.dispatch('sr/processVideo', params)

      this.$notify({
        text: 'Your video is currently being processed, this may take up to 30 minutes'
      })
    }
  },
  computed: {
    processedState() {
      if (this.video.srProcessing == true) return 1
      else if (!this.video.lrBaseURL || !this.video.hrBaseURL) return 0
      else return 2
    },
    tooltipText() {
      if (this.processedState == 1) {
        return "The video is currently being processed for super resolution"
      }
      else if (this.processedState == 0) {
        return "Process the video with super resolution"
      }
      else return "The video is processed with super resolution!"
    },
    buttonColor() {
      if (this.processedState == 1) {
        return "yellow darken-1"
      }
      else if (this.processedState == 0) {
        return "default"
      }
      else return "orange"
    },
    serverRunning() {
      return this.$store.getters['sr/running']
    }
  }
}
</script>