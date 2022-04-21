<template>
  <div class="playlist-info-container height-side bg-gray-200 flex">
    <div class="flex flex-col w-full pt-4 px-2">
      <div class="playlist-info-thumbnail-container mb-4">
        <playlist-thumbnail :playlist="playlist" :to="playAllLink" />
      </div>
      <div class="playlist-info-title-container">
        <div class="playlist-info-user-container mb-2">
          <profile-picture-and-username :user="playlist.user" />
        </div>
        <div class="playlist-info-data-container">
          <div class="flex flex-row">
            <p class="text-xs">
              {{ playlistsDataString }}
            </p>
          </div>
        </div>
        <span class="font-bold">Playlist Title:</span>
        <div class="flex flex-row my-1">
          <h1 v-if="!playlistTitleEdit" class="text-lg">
            {{ playlist.playlistTitle }}
          </h1>
          <v-text-field
            label="update playlist title"
            v-else-if="playlistTitleEdit"
            v-model="playlistTitleCopy"
            hide-details
            class="pa-0 ma-0 mt-4"
            color="#A13440"
            @keydown.enter.prevent="handleTitleEdit"
          />
          <div class="flex flex-1 justify-end">
            <v-btn icon @click="handleTitleEdit">
              <v-icon small>
                {{
                  !playlistTitleEdit
                    ? "icon-pencil-outline"
                    : "mdi-content-save"
                }}
              </v-icon>
            </v-btn>
          </div>
        </div>
      </div>

      <span class="font-bold">Playlist Description:</span>
      <div class="playlist-info-description-container">
        <div class="flex flex-row">
          <div v-if="!playlistDescriptionEdit">
            <p v-if="playlist.description">
              {{ playlist.description }}
            </p>
            <p v-else class="text-xs text-gray-700">...</p>
          </div>
          <v-textarea
            v-else
            label="update description"
            v-model="playlistDescriptionCopy"
            color="#A13440"
            rows="1"
            auto-grow
            class="pa-0 mt-4 w-full"
            hide-details
            @keydown.enter.prevent="handleDescriptionEdit"
          >
          </v-textarea>
          <div class="flex flex-1 justify-end">
            <v-btn icon class="pa-0 ma-0" @click="handleDescriptionEdit">
              <v-icon small>
                {{
                  !playlistDescriptionEdit
                    ? "icon-pencil-outline"
                    : "mdi-content-save"
                }}
              </v-icon>
            </v-btn>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PlaylistPageInfoColumn",
  props: {
    playlist: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      playlistTitleEdit: false,
      playlistTitleCopy: "",

      playlistDescriptionEdit: false,
      playlistDescriptionCopy: "",

      updating: false,
    };
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      this.playlistTitleCopy = this.playlist.playlistTitle;
      this.playlistDescriptionCopy = this.playlist.description;
    },
    handleTitleEdit() {
      this.playlistTitleEdit = !this.playlistTitleEdit;

      if (
        !this.playlistTitleEdit &&
        this.playlistTitleCopy !== this.playlist.playlistTitle
      ) {
        this.updatePlaylist({ playlistTitle: this.playlistTitleCopy });
      }
    },
    handleDescriptionEdit() {
      this.playlistDescriptionEdit = !this.playlistDescriptionEdit;

      if (
        !this.playlistDescriptionEdit &&
        this.playlistDescriptionCopy !== this.playlist.description
      ) {
        this.updatePlaylist({ description: this.playlistDescriptionCopy });
      }
    },
    async updatePlaylist(params) {
      const payload = {
        ...this.playlist,
        ...params,
      };

      const response = await this.$store.dispatch(
        "playlists/playlistsPut",
        payload
      );

      this.$store.commit("playlists/playlistUpdate", payload);

      return response;
    },
  },
  computed: {
    playlistsDataString() {
      const videosCount = this.playlist.videos.length;

      return `${videosCount} video${videosCount > 1 ? "s" : ""}`;
    },
    playAllLink() {
      if (
        !this.playlist ||
        !this.playlist.videos ||
        this.playlist.videos.length <= 0
      )
        return;
      return `/videos/pk=${this.playlist.videos[0].videoPK}&sk=${this.playlist.videos[0].videoSK}&listPK=${this.playlist.pk}&listSK=${this.playlist.sk}&index=0`;
    },
  },
};
</script>

<style scoped>
.playlist-info-container {
  max-width: 360px;
  width: 100%;
}
.height-side {
  height: calc(100vh - 76px);
}
</style>
