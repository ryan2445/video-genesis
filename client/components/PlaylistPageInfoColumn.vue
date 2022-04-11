<template>
  <div
    class="playlist-info-container h-screen bg-gray-200 flex"
  >
    <div class="flex flex-col w-full pt-4 px-2">
      <div class="playlist-info-thumbnail-container mb-4">
        <playlist-thumbnail :playlist="playlist" :to="playAllLink" />
      </div>
      <div class="playlist-info-title-container">
        <div class="flex flex-row">
          <h1 v-if="!playlistTitleEdit" class="text-lg font-bold">
            {{ playlist.playlistTitle }} 
          </h1>
          <v-text-field
            label="update playlist title"
            v-else-if="playlistTitleEdit"
            v-model="playlistTitleCopy"
            hide-details
            class="pa-0 ma-0"
            color="orange"
            @keydown.enter.prevent="handleTitleEdit"
          />
        
        <div class="flex flex-1 justify-end">
          <v-btn icon @click="handleTitleEdit">
            <v-icon small>
              {{ !playlistTitleEdit ? 'icon-pencil-outline' : 'mdi-content-save' }}
            </v-icon>
          </v-btn>
        </div>
        </div>
      </div>
      <div class="playlist-info-user-container">
        <profile-picture-and-username :user="playlist.user" />
      </div>
      <div class="playlist-info-data-container">
        <div class="flex flex-row mt-3">
          <p class="text-xs">
            {{ playlistsDataString }}
          </p>
        </div>
      </div>
      <div class="playlist-info-description-container">

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
      required: true
    }
  },
  data() {
    return {
      playlistTitleEdit: false,
      playlistTitleCopy: '',

      updating: false
    }
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      this.playlistTitleCopy = this.playlist.playlistTitle;
    },
    handleTitleEdit() {
      this.playlistTitleEdit = !this.playlistTitleEdit;

      if (!this.playlistTitleEdit && this.playlistTitleCopy !== this.playlist.playlistTitle) {
        this.updatePlaylist()
      }
    },
    async updatePlaylist() {
      const payload = {
        ...this.playlist,
        playlistTitle: this.playlistTitleCopy
      }

      const response = await this.$store.dispatch('playlists/playlistsPut', payload)

      this.$store.commit('playlists/playlistUpdate', payload)

      return response;
    }
  },
  computed: {
    playlistsDataString() {
      const videosCount = this.playlist.videos.length;

      return `${videosCount} video${videosCount > 1 ? 's' : ''}`
    },
    playAllLink() {
      return `/videos/pk=${this.playlist.videos[0].videoPK}&sk=${this.playlist.videos[0].videoSK}&listPK=${this.playlist.pk}&listSK=${this.playlist.sk}&index=0`
    }
  }
}
</script>

<style scoped>
.playlist-info-container {
  max-width: 360px;
  width: 100%;
}
</style>