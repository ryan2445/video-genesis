<template>
  <div class="mr-3">
    <v-dialog v-model="playlistsDialogBox" persistent max-width="255px">
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
      <v-card class="mx-auto" width="560" style="max-height: 500px">
        <v-card-title class="orange">
          <span class="text-h5 white--text">Save to...</span>
          <span style="float: right" @click="playlistsDialogBox = false"
            >x</span
          >
          <!-- <v-card-title>
          <span class="text-h5"> Save to... </span> -->
        </v-card-title>

        <v-card-text>
          <v-container style="max-height: 400px; overflow: auto">
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
          </v-container>
          <!-- <v-divider></v-divider> -->
          <!-- <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Enter a playlist name..."
                  type="text"
                  filled
                  v-model="newPlayListName"
                  hide-details
                  dense
                />
              </v-col>
            </v-row>
            <v-container fluid>
              <v-checkbox
                v-model="isPrivate"
                label="Private"
                @change="onChange"
                hide-details
              ></v-checkbox>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="onDialogClose">
                  Close
                </v-btn>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="createNewPlaylist(video)"
                >
                  Create
                </v-btn>
              </v-card-actions>
            </v-container>
          </v-container> -->
        </v-card-text>
        <v-card-actions>
          <v-btn @click="showPlaylistForm = true">Add new playlist </v-btn>
        </v-card-actions>

        <v-expand-transition>
          <div v-show="showPlaylistForm">
            <playlist-form
              @close="showPlaylistForm = false"
              minWidth="255"
            ></playlist-form>
          </div>
        </v-expand-transition>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import NewPlaylistButton from "./NewPlaylistButton.vue";
export default {
  name: "SaveToPlayList",
  props: {
    NewPlaylistButtonideo: {
      type: Object,
      required: true,
    },
    user: {
      type: Object,
      required: true,
    },
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
