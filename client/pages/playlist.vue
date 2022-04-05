<template>
  <div>
    <playlist-videos v-if="playlist" :playlist="playlist" />
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  name: "Playlist",
  created() {
    this.$store.commit("app/setRoute", "playlist");
  },
  data() {
    return {
      sk: null,
      pk: null,
      playlist: null,
    };
  },
  mounted() {
    this.getQueryParamsAndSetKeys();

    if (this.sk && this.pk)
      this.getPlaylist()
    else 
      this.$router.push('/home')
  },
  methods: {
    async getPlaylist() {
      console.log('getPlaylist')
      const playlist = await this.$store.dispatch("playlists/playlistGet", {
        sk: this.sk,
        pk: this.pk,
      });
      console.log('playlist', playlist)
      this.playlist = playlist;
    },
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
