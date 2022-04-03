<template>
  <div>
    <div v-if="loading">loading...</div>

    <div v-else>
      <v-row>
        <v-col v-for="playlist in playlists" :key="playlist.playlistTitle">
          <v-card class="mx-auto" max-width="344">
            <v-img
              src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
              height="200px"
              @click="onCardClick(playlist.sk, playlist.pk)"
            ></v-img>

            <v-card-title> {{ playlist.playlistTitle }} </v-card-title>
            <div>
              <v-list-item>
                <v-dialog v-model="deleteDialogBox" max-width="600px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-btn
                      top
                      class="my-1"
                      color="orange"
                      dark
                      v-bind="attrs"
                      v-on="on"
                      v-ripple="{ class: 'red--text' }"
                      style="min-width: 112px"
                      @click="setVideoSKToDelete(playlist.sk)"
                    >
                      <v-icon left> mdi-delete </v-icon>
                    </v-btn>
                  </template>
                  <div class="text-center">
                    <v-sheet
                      class="px-7 pt-7 pb-4 mx-auto text-center d-inline-block"
                      color="white"
                      dark
                    >
                      <div class="orange pa-4 bg-secondary rounded-t-xl">
                        Are you sure you want to delete this playlist?
                      </div>

                      <v-btn
                        class="ma-1"
                        elevation="12"
                        height="25"
                        width="1%"
                        color="orange"
                        plain
                        @click.stop="onDeleteDialogClose"
                      >
                        Cancel
                      </v-btn>

                      <v-btn
                        class="mx-auto transition-swing secondary"
                        elevation="12"
                        height="25"
                        width="1%"
                        color="orange"
                        plain
                        @click="onPlaylistDeleteConfirmation"
                      >
                        Delete
                      </v-btn>
                    </v-sheet>
                  </div>
                </v-dialog>
              </v-list-item>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";

import "material-design-icons-iconfont/dist/material-design-icons.css"; // Ensure you are using css-loader
import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

export default {
  icons: {
    iconfont: "md",
  },
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
    async playlistsGet() {},
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
