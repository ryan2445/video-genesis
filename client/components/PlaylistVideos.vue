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
    this.videos = this.playlist["videos"]["Items"];
  },
};
</script>
