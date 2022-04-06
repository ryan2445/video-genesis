<template>
  <div class="mr-3">
    <v-dialog v-model="playlistsDialogBox" persistent max-width="300px">
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
          @click="UpdatePlaylist(video.sk)"
        >
          <v-icon>icon-playlist-plus</v-icon>
        </v-btn>
      </template>
      <v-card>
        <v-card-title>
          <span class="text-h5"> Save to... </span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <form @submit.prevent="handlePlaylistSubmit" class="playlist-form">
              <div
                class="form-group form-check"
                v-for="item in playlist"
                v-bind:key="item.id"
              >
                <v-checkbox
                  :value="item"
                  v-model="namesOfThePlaylists"
                  :label="item.playlistTitle"
                ></v-checkbox>
              </div>

              <div class="form-group">
                <button class="btn btn-primary">Submit</button>
              </div>
            </form>
          </v-container>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Create a new playlist"
                  type="text"
                  filled
                  v-model="newPlayListName"
                />
              </v-col>
            </v-row>
            <v-container fluid>
              <v-checkbox
                v-model="isPrivate"
                label="Make the Playlist Private"
                @change="onChange"
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
          </v-container>
        </v-card-text>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
export default {
  name: "SaveToPlayList",
  props: {
    playlist: {
      type: Array,
      required: true,
    },
    video: {
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
      namesOfThePlaylists: [],
      isPrivate: false,
      newPlayListName: null,
      playlistsDialogBox: false,
    };
  },
  methods: {
    async handlePlaylistSubmit() {
      for (let index = 0; index < this.playlist.length; index++) {
        await this.removeVideoFromPlaylist(
          this.playlist[index].sk,

          [
            {
              sk: this.video.sk,
              pk: this.video.pk,
            },
          ]
        );
      }

      for (let index = 0; index < this.namesOfThePlaylists.length; index++) {
        await this.addVideoToPlaylist(this.namesOfThePlaylists[index].sk, [
          {
            sk: this.video.sk,
            pk: this.video.pk,
          },
        ]);
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
      //  Create playlist
      await this.$store.dispatch("playlists/playlistsPost", {
        playlistTitle: this.newPlayListName,
        isPrivate: this.isPrivate,
        video: video,
      });
      this.playlistsDialogBox = false;
    },

    async UpdatePlaylist(videoSk) {
      let namesOfThePlaylists = [];
      for (let index = 0; index < this.playlist.length; index++) {
        const playlistNames = await this.$store.dispatch(
          "playlists/playlistGet",
          {
            pk: "ID#" + this.user.username,
            sk: this.playlist[index].sk,
          }
        );
        if (playlistNames.videos.find((value) => value.videoSK == videoSk)) {
          namesOfThePlaylists.push(this.playlist[index]);
        }
      }
      this.namesOfThePlaylists = namesOfThePlaylists;
    },
    async addVideoToPlaylist(playlistKey, videos) {
      await this.$store.dispatch("playlists/playlistAddVideos", {
        sk: playlistKey,
        videos,
      });
    },
    async removeVideoFromPlaylist(playlistKey, videos, videoToRemove) {
      await this.$store.dispatch("playlists/playlistDeleteVideos", {
        sk: playlistKey,
        videos,
      });
    },
  },
};
</script>
