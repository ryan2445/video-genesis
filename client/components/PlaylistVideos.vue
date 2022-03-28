<template>
  <div>
    <v-row class="justify-center">
      <div v-for="(video, index) in videoCardsVideo" :key="index">
        <video-card :video="video" />
      </div>
    </v-row>
  </div>
</template>
<script>
import { mapGetters } from "vuex";

export default {
  props: {
    playlist: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      videos: [],
      videoCardsVideo: [],
    };
  },

  computed: {
    ...mapGetters({
      user: "user/user",
    }),
  },
  async mounted() {
    const videos = await this.$store.dispatch("videos/videosGetByUsername", {
      username: this.user.username,
    });
    this.videos = videos;

    const videoSks = String(this.playlist.videos).split(",");

    let videoCardsVideo = [];

    videos.forEach((video) => {
      if (videoSks.includes(video.sk)) {
        videoCardsVideo.push(video);
      }
    });

    this.videoCardsVideo = videoCardsVideo;
  },
};
</script>
