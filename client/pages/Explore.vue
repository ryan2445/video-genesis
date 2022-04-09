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
    <video-list :videos="videosOnCurrentPage || []" />
    <div class="text-xs-center">
      <v-pagination
        color="orange"
        v-model="page"
        :length="paginationLength"
        @input="paginate"
      ></v-pagination>
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
      page: 1,
      videosOnCurrentPage: null,
      videosPerPage: 8,
      paginationLength: null,
    };
  },
  computed: {
    ...mapGetters({
      videos: "videos/videos",
    }),
  },
  methods: {
    async paginate(pageNumber) {
      let startingIndex = 0;
      let lastIndex = 0;
      startingIndex = (pageNumber - 1) * this.videosPerPage;
      lastIndex = startingIndex + this.videosPerPage;

      if (this.videos.length < lastIndex) {
        this.videosOnCurrentPage = this.videos.slice(
          startingIndex,
          this.videos.length
        );
      } else {
        this.videosOnCurrentPage = this.videos.slice(startingIndex, lastIndex);
      }
    },
  },

  created() {
    this.$store.commit("app/setRoute", "Explore");
  },
  async mounted() {
    //  Send request to get videos
    await this.$store.dispatch("videos/getAllVideos");

    //  Stop loading
    this.loading = false;
    this.paginationLength = Math.ceil(this.videos.length / this.videosPerPage);
    if (this.videos.length > this.videosPerPage) {
      this.videosOnCurrentPage = this.videos.slice(0, this.videosPerPage);
    } else {
      this.videosOnCurrentPage = this.videos.slice(0, this.videos.length);
    }
  },
};
</script>

<style scoped></style>
