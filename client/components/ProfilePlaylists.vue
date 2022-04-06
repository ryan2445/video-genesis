<template>
  <div class="mt-3 relative">
    <new-playlist-button />
    <v-row class="relative" v-if="playlists" justify="center" align="center" >
      <v-col>
        <div 
          v-for="(playlist, i) in playlists"
          :key="playlist.sk"
          class="flex flex-1 flex-col"
        >
          <playlist-card :playlist="playlist" @playlist:deleted="onPlaylistDeleted"></playlist-card>
          <v-divider v-if="i !== playlists.length - 1"  />
        </div>
      </v-col>
    </v-row>
  </div>
</template>
<script>
import { mapGetters } from "vuex";

export default {
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      loading: true,
      videoSKToDelete: null,

      playlistNames: null,
      playlistVideos: [],
      deleteDialogBox: false,

      showPlaylistForm: false
    };
  },
  async mounted() {
    await this.getPlaylists()

    //  Stop loading
    this.loading = false;
  },
  computed: {
    ...mapGetters({
      playlists: "playlists/playlists",
    })
  },
  methods: {
    async getPlaylists() {
      const playlists = await this.$store.dispatch(
        "playlists/playlistsGetByUsername",
        {
          username: this.user.username,
        }
      );

      this.$store.commit("playlists/playlistsSet", playlists);
    },
    async onPlaylistDeleteConfirmation() {
      await this.$store.dispatch("playlists/playlistsDelete", {
        sk: this.videoSKToDelete,
      });

      await this.getPlaylists()
      
      this.deleteDialogBox = false;
    },
    async setVideoSKToDelete(playlistSK) {
      this.videoSKToDelete = playlistSK;
    },
    async onDeleteDialogClose() {
      this.deleteDialogBox = false;
    },
    async onPlaylistDeleted(playlist) {
      
    }
  },
};
</script>
