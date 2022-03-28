<template>
  <div>
    <playlist-videos v-if="playlist" :playlist="playlist" />
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  created() {
    this.$store.commit("app/setRoute", "playlist");
  },
  data() {
    return {
      sk: undefined,
      playlist: undefined,
    };
  },
  async mounted() {
    await this.$store.dispatch("playlists/playlistsGet");
    this.getQueryParamsAndSetKeys();
    console.log(this);
  },
  methods: {
    getQueryParamsAndSetKeys() {
      const path = this.$route.fullPath.replace("/playlist", "");
      const params = new URLSearchParams(path);

      // If the sk is not provided, error
      if (!params.has("sk")) {
        console.error("sort key not provided");
        return;
      }

      const sk = params.get("sk");

      this.sk = sk;

      for (let index = 0; index < this.playlists.length; index++) {
        var element = this.playlists[index];
        if (element.sk == this.sk) {
          this.playlist = element;
          break;
        }
      }
    },
  },

  computed: {
    ...mapGetters({
      playlists: "playlists/playlists",
      get_video_by_id: "videos/get_video_by_id",
    }),
  },
};
</script>
