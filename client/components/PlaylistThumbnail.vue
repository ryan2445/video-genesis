<template>
  <v-hover v-slot="{ hover }">
      <div @click="handleThumbnailClick" class="playlist-thumbnail-container rounded-md relative mr-2"
        :class="{'cursor-pointer' : !!to}"      
      >
        <img 
          v-if="thumbnail"
          class="playlist-thumbnail w-full h-full object-fill" 
          :src="thumbnail" 
          :alt="`${playlist.playlistTitle} thumbnail`"
        />
        <alternate-video-thumbnail v-else />
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
        <div v-if="hover && !!to" class="playlist-thumbnail-play-all-container absolute inset-0 w-full h-full grid place-items-center">
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
</template>

<script>
export default {
  name: "PlaylistThumbnail",
  props: {
    playlist: {
      type: Object,
      required: true
    },
    to: {
      type: String,
      required: false,
      default: null
    }
  },
  data() {
    return {
      thumbnail: null
    }
  },
  mounted() {
    this.getFirstThumbnail()
  },
  methods: {
    // Gets and sets the thumbnail of the playlist
    getFirstThumbnail() {
      for (let i = 0; i < this.playlist.videos.length; i++) {
        const video = this.playlist.videos[i].video

        if (video.videoThumbnail) {
          this.thumbnail = video.videoThumbnail
          return
        }
      }
    },
    handleThumbnailClick() {
      if (!this.to) return

      this.$router.push(this.to)
    }
  },
  computed: {
    videosCount() {
      return this.playlist.videos.length
    },
  },
  watch: {
    playlist(newVal) {
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
</style>