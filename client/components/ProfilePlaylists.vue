<template>
  <div>
    <h1>Playlists</h1>
    <div v-if="loading">loading...</div>

    <div v-else>
      <v-row>
        <v-col v-for="playlist in playlists" :key="playlist.playlistTitle">
          <v-card class="mx-auto" max-width="344">
            <v-img
              src="https://cdn.vuetifyjs.com/images/cards/sunshine.jpg"
              height="200px"
              @click="onCardClick(playlist.sk)"
            ></v-img>

            <v-card-title> {{ playlist.playlistTitle }} </v-card-title>

            <v-btn
              color="orange"
              dark
              v-bind="attrs"
              v-on="on"
              v-ripple="{ class: 'red--text' }"
              @click="onPlaylistDelete(playlist.sk)"
            >
              <span class="material-icons"> delete </span>
            </v-btn>
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
  data() {
    return {
      loading: true,

      playlistNames: null,
      playlistVideos: [],
      deleteDialogBox: false,
    };
  },
  async mounted() {
    //  Send request to get videos
    await this.$store.dispatch("playlists/playlistsGet");

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
    onCardClick(sk) {
      this.$router.push(`/playlist?sk=${sk}`);
    },
    async onPlaylistDelete(playlistSK) {
      // alert(playlistSK);
      await this.$store.dispatch("playlists/playlistsDelete", {
        sk: playlistSK,
      });
      this.$forceUpdate();

      this.deleteDialogBox = false;
    },
    async onDeleteDialogClose() {
      this.deleteDialogBox = false;
    },
  },
};
</script>
