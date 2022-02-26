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
    <div class="grid md:grid-cols-3 grid-cols-1 gap-x-2 items-center place-items-center">
      <video-card v-for="(video, i) in videos" :key="i" :video="video" :idx="i" />
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
  name: "Explore",
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
  created() {
    this.$store.commit('app/setRoute', "Explore")
  },
  async mounted() {
    //  Send request to get videos
    await this.$store.dispatch("videos/getAllVideos");

    //  Stop loading
    this.loading = false;
  },
};
</script>

<style scoped></style>
