<template>
  <div 
    v-if="playlistFull"
    class="flex flex-row w-full my-3" 
  >
    <playlist-thumbnail 
      :playlist="playlistFull"
      :to="playlistThumbnailLink" 
    />
    <div class="playlist-info-container py-2">
      <div class="playlist-title text-base font-bold">
        <h1>
          {{ playlist.playlistTitle }}
        </h1>
      </div>
      <playlist-card-user-link 
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
    <div
      class="flex flex-1"
      v-if="permission"
    >
      <div class="ml-auto my-auto mr-3">
        <NuxtLink
          :to="`playlists?pk=${playlist.pk}&sk=${playlist.sk}`"
        >
          <v-btn
            icon
          >
            <v-icon>
              icon-pencil-outline
            </v-icon>
          </v-btn>
        </NuxtLink>
        <v-btn
          icon
          @click="onDelete"
          :loading="deleting"
          :disabled="deleting"
        >
          <v-icon>
            icon-delete
          </v-icon>
        </v-btn>
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
    },
    permission: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      playlistFull: null,
      thumbnail: null,
      deleting: false,
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
    },
    async onDelete() {
      this.deleting = true

      try {
        const params = {
          pk: this.playlistFull.pk,
          sk: this.playlistFull.sk
        }

        await this.$store.dispatch('playlists/playlistsDelete', params)

        this.$emit('playlist:deleted', this.playlistFull)
      }
      catch(e) {
        console.error('Playlist delete error')
      }
      finally {
        this.deleting = false
      }
    }
  },
  computed: {
    latestVideos() {
      if (!this.playlistFull) return null

      const latestVideosTitles = []

      for (let i = 0; i < Math.min(this.playlistFull.videos.length, 2); i++) {
        const video = this.playlistFull.videos[i]

        if (!video.video) continue

        latestVideosTitles.push({
          title: video.video.videoTitle,
          to: `videos/pk=${video.videoPK}&sk=${video.videoSK}`
        })
      }

      return latestVideosTitles
    },
    playlistThumbnailLink() {
      if (!this.playlistFull) return null
      if (this.playlistFull.videos.length === 0) {
        return `playlists?pk=${this.playlist.pk}&sk=${this.playlist.sk}`
      }

      return `/videos/pk=${this.playlistFull.videos[0].videoPK}&sk=${this.playlistFull.videos[0].videoSK}&list=${this.playlist.sk}&index=0`

    }
  }
}
</script>

<style scoped>

</style>