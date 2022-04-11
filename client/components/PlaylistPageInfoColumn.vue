<template>
  <div
    class="playlist-info-container h-screen bg-gray-200 flex"
  >
    <div class="flex flex-col w-full pt-4 px-2">
      <div class="playlist-info-thumbnail-container mb-4">
        <playlist-thumbnail :playlist="playlist" :to="playAllLink" />
      </div>
      <div class="playlist-info-title-container w-full mt">
        <h1 class="text-lg font-bold">
          {{ playlist.playlistTitle }} 
        </h1>
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
  mounted() {

  },
  computed: {
    playlistsDataString() {
      const videosCount = this.playlist.videos.length;

      return `${videosCount} video${videosCount > 1 ? 's' : ''}`
    },
    playAllLink() {
      return `/videos/pk=${this.playlist.videos[0].videoPK}&sk=${this.playlist.videos[0].videoSK}&list=${this.playlist.sk}&index=0`
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