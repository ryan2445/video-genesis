<template>
  <div class="mr-3">
    <v-dialog class="relative" v-model="playlistsDialogBox" width="440px" >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          v-bind="attrs"
          v-on="on"
          fab
          depressed
          color="grey lighten-1"
          width="30"
          height="30"
          class="mb-2 shadow-md justify-right"
        >
          <v-icon>icon-playlist-plus</v-icon>
        </v-btn>
      </template>
      <v-card class="mx-auto relative" style="max-height: 640px;">
        <v-btn
          absolute
          class="top-0 right-0"
          @click="playlistsDialogBox = false"
          icon
        >
          <v-icon>
            icon-close
          </v-icon>
        </v-btn>
        <v-card-title class="orange">
          <span class="text-h5 white--text">Save to...</span>
        </v-card-title>
        <v-card-text>
          <div
            class="form-group form-check"
            v-for="item in playlists"
            v-bind:key="item.id"
          >
            <v-checkbox
              @change="onPlaylistSelected(item)"
              :value="item"
              v-model="selectedPlaylists"
              :label="item.playlistTitle"
            ></v-checkbox>
          </div>
        </v-card-text>
        <v-card-actions
          v-if="!showPlaylistForm"
          class="orange"
        >
          <v-btn text @click="showPlaylistForm = true"
            >Create new playlist
          </v-btn>
        </v-card-actions>
        <v-card-title v-else class="orange">
          <div>
            Create playlist
          </div>
        </v-card-title>
        <v-expand-transition>
          <div v-show="showPlaylistForm">
            <playlist-form
              :video="video"
              @close="showPlaylistForm = false"
              minWidth="255"
            >
            </playlist-form>
          </div>
        </v-expand-transition>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  name: "SaveToPlayList",
  props: {
    video: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      selectedPlaylists: [],
      isPrivate: false,
      newPlayListName: null,
      playlistsDialogBox: false,
      showPlaylistForm: false,
    };
  },
  created() {
    if (this.playlistsDialogBox) this.getPlaylists();
  },
  methods: {
    onPlaylistSelected(playlist) {
      const index = this.selectedPlaylists.findIndex(
        (p) => p.pk == playlist.pk && p.sk == playlist.sk
      );

      const addToPlaylist = index != -1;

      if (addToPlaylist) {
        this.addVideoToPlaylist(playlist);
      } else {
        this.removeVideoFromPlaylist(playlist);
      }
    },
    async onDialogClose() {
      this.playlistsDialogBox = false;
    },
    onChange() {
      this.$emit("update", {
        isPrivate: this.isPrivate,
      });
    },
    async createNewPlaylist(video) {
      // Do not continue if the video does not exist, or the video is null
      if (!video || !this.newPlayListName) return;

      //  Create playlist
      await this.$store.dispatch("playlists/playlistsPost", {
        playlistTitle: this.newPlayListName,
        isPrivate: this.isPrivate,
        video: video,
      });
      this.playlistsDialogBox = false;
    },
    async addVideoToPlaylist(playlist) {
      await this.$store.dispatch("playlists/playlistAddVideos", {
        sk: playlist.sk,
        videos: [this.video],
      });
    },
    async removeVideoFromPlaylist(playlist) {
      await this.$store.dispatch("playlists/playlistDeleteVideos", {
        sk: playlist.sk,
        videos: [this.video],
      });
    },
    async getPlaylists() {
      await this.$store.dispatch("playlists/playlistsGet");
    },
  },
  computed: {
    ...mapGetters({
      playlists: "playlists/playlists",
    }),
  },
  watch: {
    playlistsDialogBox(val) {
      if (val && !this.playlists) {
        this.getPlaylists();
      }
    },
  },
};
</script>
