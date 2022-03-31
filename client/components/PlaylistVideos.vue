<template>
  <div>
    <v-row class="justify-center">
      <div v-for="(video, index) in videos" :key="index">
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
      videos2: "videos/videos",
      user: "user/user",
    }),
  },
  async mounted() {
    this.videos = this.playlist["videos"]['Items'];
    console.log("here<<<", this.videos, this.videos2);
    // await this.$store.dispatch("videos/getAllVideos");
    // var userVideos = await this.$store.dispatch("videos/videosGetByUsername", {
    //   username: this.user.username,

    // console.log("explore videos");
    // console.log(this.videos);
    // console.log("user videos");
    // console.log(userVideos);
    // console.log("end");

    // const videoSks = String(this.playlist.videos).split(",");
    // console.log(videoSks);

    // let videoCardsVideo = [];

    // // view videos from other users
    // this.videos.forEach((video) => {
    //   if (videoSks.includes(video.sk)) {
    //     videoCardsVideo.push(video);
    //     alert("pushed a video");
    //   }
    // });

    // // view users own videos
    // userVideos.forEach((video) => {
    //   if (videoSks.includes(video.sk)) {
    //     videoCardsVideo.push(video);
    //     alert("pushed a video");
    //   }
    // });

    //   this.videoCardsVideo = videoCardsVideo;
  },
};
</script>
