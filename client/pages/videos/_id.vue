<template>
  <v-container class="">
    <v-row>
      <v-col>
        <template v-if="!loading">
          <VideoPlayer :video-data="videoData" :audio="videoAudio" />
          <video-player-info :video="video" />
        </template>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import VideoPlayerInfo from "../../components/VideoPlayerInfo.vue";
export default {
  name: "VideoCard",
  layout: "dashboard",
  components: { VideoPlayerInfo },
  data() {
    return {
      sk: this.$route.params.id,
      bucket_url:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      video: null,
      loading: true,
    };
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
    const sk = `VIDEO#${this.sk}`;

    await this.$store.dispatch("videos/videosGet");

    const video = this.$store.getters["videos/videos"].find(
      (video) => video.sk == sk
    );

    this.video = video;

    this.loading = false;
  },
};
</script>

<style></style>
