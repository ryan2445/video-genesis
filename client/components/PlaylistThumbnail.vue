<template>
  <v-hover v-slot="{ hover }">
    <NuxtLink :to="to">
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
    </NuxtLink>
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
      required: true
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
.thumbnail-blank {
  background: radial-gradient(circle at center, orange 0, black 80%);
}
</style>