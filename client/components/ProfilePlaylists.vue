<template>
  <div class="mt-3">
    <v-row class="relative" v-if="playlists" justify="center" align="center" >
      <v-menu v-model="showPlaylistForm" offset-y nudge-left="435" nudge-bottom="2" :close-on-content-click="false">
        <template v-slot:activator="{ on, attrs }">
          <v-btn
            absolute
            right top
            v-bind="attrs"
            v-on="on"
          >
            <span class="text-app-orange">
              New Playlist
            </span>
          </v-btn>
        </template>
        <playlist-form @close="showPlaylistForm = false"></playlist-form>
      </v-menu>
      <v-col>
        <div 
          v-for="(playlist, i) in playlists"
          :key="playlist.sk"
          class="flex flex-1 flex-col"
        >
          <playlist-card :playlist="playlist"></playlist-card>
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
    console.log(this.user);
    const playlists = await this.$store.dispatch(
      "playlists/playlistsGetByUsername",
      {
        username: this.user.username,
      }
    );
    this.$store.commit("playlists/playlistsSet", playlists);

    //  Stop loading
    this.loading = false;
  },
  computed: {
    ...mapGetters({
      playlists: "playlists/playlists",
      get_video_by_id: "videos/get_video_by_id",
    }),
  },
  methods: {
    async playlistsGet() { },
    onCardClick(sk, pk) {
      this.$router.push(`/playlist?sk=${sk}&pk=${pk}`);
    },
    async onPlaylistDeleteConfirmation() {
      // alert(this.videoSKToDelete);
      await this.$store.dispatch("playlists/playlistsDelete", {
        sk: this.videoSKToDelete,
      });
      this.deleteDialogBox = false;
    },
    async setVideoSKToDelete(playlistSK) {
      this.videoSKToDelete = playlistSK;
    },
    async onDeleteDialogClose() {
      this.deleteDialogBox = false;
    },
  },
};
</script>
