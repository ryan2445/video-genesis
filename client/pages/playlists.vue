<template>
  <div class="flex flex-row w-screen">
    <playlist-page-info-column v-if="playlist" :playlist="playlist" />
    <playlist-table v-if="playlist" :playlist="playlist" />
  </div>
</template>

<script>
export default {
  name: "playlists",
  layout: "dashboard",
  data() {
    return {
      pk: null,
      sk: null,
      playlist: null,
    };
  },
  mounted() {
    this.getQueryParamsAndSetKeys();
    this.getPlaylist();
  },
  methods: {
    getQueryParamsAndSetKeys() {
      const path = this.$route.fullPath?.replace("/playlists?", "");
      const params = new URLSearchParams(path);

      // If the sk is not provided, error
      if (!params.has("sk")) {
        console.error("sort key not provided");
        return;
      }

      this.sk = params.get("sk");
      this.pk = params.get("pk");
    },
    async getPlaylist() {
      const params = {
        pk: this.pk,
        sk: this.sk,
      };

      const playlist = await this.$store.dispatch(
        "playlists/playlistGet",
        params
      );

      this.playlist = playlist;
    },
  },
};
</script>
