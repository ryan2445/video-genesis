<template>
  <div class="flex flex-row w-full my-3">
    <v-hover v-slot="{ hover }">
      <div class="playlist-thumbnail-container rounded-md relative mr-2 cursor-pointer">
        <img 
          v-if="thumbnail"
          class="playlist-thumbnail w-full h-full object-fill" 
          :src="thumbnail" 
          :alt="`${playlist.playlistTitle} thumbnail`"
        />
        <div
          v-else
          class="playlist-thumbnail thumbnail-blank w-full h-full grid place-content-center"
        >
          <v-icon color="white" large>
            icon-video
          </v-icon>
        </div>
        <div class="playlist-thumbnail-views-container absolute right-0 top-0 bottom-0 h-full grid place-items-center px-2">
          <div class="flex flex-col">
            <div>
              <p class="text-white text-center select-none">
                {{ videosCount }}
              </p>
            </div>
            <div>
              <v-icon color="white">
                icon-playlist-play
              </v-icon>
            </div>
          </div>
        </div>
        <div v-if="hover" class="playlist-thumbnail-play-all-container absolute inset-0 w-full h-full grid place-items-center">
          <div class="flex flex-row">
            <div>
              <v-icon color="white" left>
                icon-play
              </v-icon>
            </div>
            <div>
              <p class="text-white select-none">
                PLAY ALL
              </p>
            </div>
          </div>
        </div>
      </div>
    </v-hover>
    <div class="playlist-info-container py-2">
      <div class="playlist-title text-base font-bold">
        <h1>
          {{ playlist.playlistTitle }}
        </h1>
      </div>
      <div
        class="playlist-user"
        v-if="user"
      >
        <NuxtLink :to="`users/username=${playlist.pk.substr(3)}`">
          <h2
            class="text-xs text-gray-700"
          >
            {{ user | userDisplayName }}
          </h2>
        </NuxtLink>
      </div>
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
      user: null
    }
  },
  async mounted() {
    this.getUser()
    await this.getPlaylistVideos()
    this.getFirstThumbnail()
    
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
    // Gets and sets the thumbnail of the playlist
    getFirstThumbnail() {
      for (let i = 0; i < this.playlistFull.videos.length; i++) {
        const video = this.playlistFull.videos[i].video

        if (video.videoThumbnail) {
          this.thumbnail = video.videoThumbnail
          return
        }
      }
    },
    async getUser() {
      const username = this.playlist.pk.substr(3)
      const user = await this.$store.dispatch('users/userGetByUsername', username)
      this.user = user
    }
  },
  computed: {
    videosCount() {
      if (!this.playlistFull) return 0

      return this.playlistFull.videos.length
    },
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
  },
  watch: {
    playlistFull(newVal) {
      this.getFirstThumbnail()
    }
  }
}
</script>

<style scoped>
.playlist-thumbnail-container {
  width: 246px;
  height: 138px;
}
.playlist-thumbnail-views-container {
  background: rgba(0, 0, 0, 0.575);
}
.playlist-thumbnail-play-all-container {
  background: rgba(0, 0, 0, 0.80);
}
.thumbnail-blank {
  background: radial-gradient(circle at center, orange 0, black 80%);
}
</style>