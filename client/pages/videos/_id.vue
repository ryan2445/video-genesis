<template>
  <v-container class="">
    <v-row>
      <v-col>
        <template v-if="!loading">
          <VideoPlayer :src="url" :audiourl="audiourl" :video="video" />
          <video-player-info :video="video" />
        </template>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import VideoPlayerInfo from "../../components/VideoPlayerInfo.vue";
var audiourl = null;
export default {
  name: "VideoCard",
  layout: "dashboard",
  components: { VideoPlayerInfo },
  data() {
    return {
      sk: this.$route.params.id,
      bucket_url:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      video: {},
      loading: true,
      url: "",
      audiourl: "",
    };
  },

  computed: {
    ...mapGetters({
      user: "user/user",
    }),
  },
  async mounted() {
    const sk = `VIDEO#${this.sk}`;
    await this.$store.dispatch("videos/videosGet");
    let video = this.$store.getters["videos/videos"].find(
      (video) => video.sk == sk
    );

    this.video = video;
    this.url = `${this.bucket_url}/${video.videoKey}/${video.videoKey}_3000.mp4`;
    this.audiourl = `${this.bucket_url}/${video.videoKey}/${video.videoKey}.mp4`;
    console.log(video, this.url);
    this.loading = false;
    var videoInfoes = JSON.parse(video.videoData);
    Array.from(videoInfoes).forEach((videoInfo) =>
      console.log("video resolution", videoInfo.width)
    );
  },
};
</script>

<style></style>
