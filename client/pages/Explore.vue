// This is not working rn, need to figure out the python deployment thing, but
it should bring all videos to Explore page!

<template>
  <div>
    <div v-if="loading" class="text-center" style="height: 100vh">
      <v-progress-circular indeterminate color="orange" style="top: 50%" />
    </div>
    <div
      v-if="!loading && videos && !videos.length"
      class="text-center"
      style="
        display: flex;
        height: 50vh;
        align-items: center;
        justify-content: center;
      "
    >
      <div>No videos found</div>
    </div>
    <div v-for="(video, i) in videos" :key="i">
      <video-card :video="video" />
    </div>
  </div>
  <!-- <VideoList /> -->
</template>

<script>
import { mapGetters } from "vuex";
import VideoCard from "../components/VideoCard.vue";
export default {
  components: { VideoCard },
  layout: "dashboard",
  data() {
    return {
      //  Controls v-progress-circular
      loading: true,
    };
  },
  computed: {
    ...mapGetters({
      videos: "videos/videosAll",
    }),
  },
  async mounted() {
    //  Send request to get videos
    await this.$store.dispatch("videos/GetAllVideos");
    alert("Hello Ji");
    console.log(this.$store.getters["videos/videosAll"]);

    //  Stop loading
    this.loading = false;
  },
};
</script>

<style scoped></style>
