<template>
  <div class="flex flex-row w-full my-3">
    <playlist-thumbnail 
      v-if="playlistFull" 
      :playlist="playlistFull"
      :to="`playlists?pk=${playlist.pk}&sk=${playlist.sk}`" 
    />
    <div class="playlist-info-container py-2">
      <div class="playlist-title text-base font-bold">
        <h1>
          {{ playlist.playlistTitle }}
        </h1>
      </div>
      <playlist-card-user-link 
        v-if="playlistFull" 
        :user="playlistFull.user" 
      />
      <div
        v-if="latestVideos"
        class="latest-videos-container mt-3 flex flex-col"
      >
        <div
          v-for="(latestVideo, i) of latestVideos"
          :key="`latest-video-${i}`"
        >
          <NuxtLink :to="latestVideo.to">
          <p
            class="text-xs text-gray-900"
          >
            {{ latestVideo.title }}
          </p>
        </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "PlaylistCard",
  props: {
    playlist: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      playlistFull: null,
      thumbnail: null,
    }
  },
  async mounted() {
    await this.getPlaylistVideos()
  },
  methods: {
    async getPlaylistVideos() {
      const params = {
        pk: this.playlist.pk,
        sk: this.playlist.sk
      }
      const playlist = await this.$store.dispatch('playlists/playlistGet', params)

      this.playlistFull = playlist
    }
  },
  computed: {
    latestVideos() {
      if (!this.playlistFull) return null

      const latestVideosTitles = []

      for (let i = 0; i < Math.min(this.playlistFull.videos.length, 2); i++) {
        const video = this.playlistFull.videos[i]

        latestVideosTitles.push({
          title: video.video.videoTitle,
          to: `videos/pk=${video.videoPK}&sk=${video.videoSK}`
        })
      }

      return latestVideosTitles
    }
  }
}
</script>

<style scoped>

</style>