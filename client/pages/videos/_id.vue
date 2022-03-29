<template>
  <v-row justify="center">
    <v-col>
      <template v-if="!loading">
        <video-container
          :video="video"
          :audio="videoAudio"
          :start-time="startTime"
          :video-data="videoData"
        >
        </video-container>
      </template>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  layout: "dashboard",
  data() {
    return {
      bucket_url:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      video: null,
      loading: true,
      pk: null,
      sk: null,
      startTime: null
    };
  },
  created() {
    this.$store.commit('app/setRoute', "")
  },
  computed: {
    ...mapGetters({
      user: "user/user",
    }),
    videoData() {
      // If the video is not loaded, return null
      if (!this.video) {
        return null;
      }

      this.$store.commit('app/setRoute', this.video.videoTitle)
      
      // Parse the videoData json string
      const json = JSON.parse(this.video.videoData);

      // If the json cannot be parsed,
      if (!json) {
        console.error("videoData undefined. There is an issue with the video data json string")
        return null
      }

      const data = json.map(data => {
        return {
          type: "video/mp4",
          src: `${this.bucket_url}/${this.video.videoKey}/${data.baseURL}`,
          label: `${data.width}`,
          res: data.width,
        }
      })

      return data
    },
    videoAudio() {
      if (!this.video || !this.bucket_url) {
        return null;
      }

      return `${this.bucket_url}/${this.video.videoKey}/${this.video.videoKey}.mp4`;
    }
  },
  async mounted() {
    this.getQueryParamsAndSetKeys();

    await this.getAndSetVideo();

    this.loading = false;
  },
  methods: {
    getQueryParamsAndSetKeys() {
      const path = this.$route.fullPath.replace('/videos/', '');
      const params = new URLSearchParams(path);

      // If the sk is not provided, error
      if (!params.has('sk')) {
        console.error('sort key not provided')
        return;
      }

      const pk = params.has('pk') 
                  ? params.get('pk') 
                  : this.$store.getters('user/user').id;
      const sk = params.get('sk');
      const time = params.get('time')

      this.pk = pk
      this.sk = sk
      this.startTime = time
    },
    async getAndSetVideo() {
      if (!this.pk || !this.sk) {
        console.error("Cannot get video without pk and sk");
        return;
      }

      const video = await this.$store.dispatch("videos/videoGet", {
        pk: this.pk,
        sk: this.sk
      });
      
      this.video = video;
    }
  }
};
</script>

<style></style>
