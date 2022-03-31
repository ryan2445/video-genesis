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
      pk: undefined,
      playlist: undefined,
    };
  },
  async mounted() {
    this.getQueryParamsAndSetKeys();
    if (this.sk) {
      const playlist = await this.$store.dispatch("playlists/playlistGet", {
        sk: this.sk,
        pk: this.pk,
      });
      this.playlist = playlist;
    }
    //await this.$store.dispatch("playlists/playlistsGet");
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

      this.sk = params.get("sk");
      this.pk = params.get("pk");
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
