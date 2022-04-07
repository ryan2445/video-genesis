<template>
  <div className="playlist-table-container w-full h-screen flex flex-1 flex-grow bg-white"
    style="width: 100%; background: white; height: 100%;"
  >
    <div
      class="w-full"
    >
      <v-list
        flat
        width="100%"
      >
        <v-subheader>
          Videos
        </v-subheader>
        <v-divider />
        <v-list-item
          v-for="(playlistItem) of playlist.videos"
          :key="`${playlistItem.sk}`"
        >
          <v-list-item-icon>
            <video-thumbnail
              :video="playlistItem.video"
              :thumbnailSrc="playlistItem.video.videoThumbnail"
              :videoSrc="`${bucket_url}/${playlistItem.video.videoKey}/${playlistItem.video.videoKey}_1500.mp4`"
              :video-key="playlistItem.video.videoKey"
              :height="90"
              :width="160"
              @click="onThumbnailClick(playlistItem.video)"
              class="cursor-pointer"
            />
          </v-list-item-icon>
          <v-list-item-content two-line>
            <v-list-item-title>
              <NuxtLink :to="`videos/pk=${playlistItem.video.pk}&sk=${playlistItem.video.sk}`">
                <div class="text-gray-800 cardTitle">
                    {{ playlistItem.video.videoTitle }}
                </div>
              </NuxtLink>
            </v-list-item-title>
            <v-list-item-subtitle>
              <NuxtLink :to="`users/username=${playlist.user.pk.substr(3)}`">
                <div>
                  {{ playlist.user | userDisplayName }}
                </div>
              </NuxtLink>
            </v-list-item-subtitle>
          </v-list-item-content>

          <v-list-item-action>
            <v-btn
              icon
              @click="onDelete(playlistItem.video)"
              :loading="deleting"
              :disabled="deleting"
            >
              <v-icon>
                icon-delete
              </v-icon>
            </v-btn>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </div>
  </div>
</template>

<script>
export default {
  name: "PlaylistTable",
  props: {
    playlist: {
      required: true,
      type: Object
    }
  },
  data() {
    return {
      bucket_url: "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      deleting: false
    }
  },
  methods: {
    onThumbnailClick(video) {
      this.$router.push(
        `/videos/pk=${video.pk}&sk=${video.sk}`
      )
    },
    async onDelete(video) {
      this.deleting = true

      try {
        const params = {
          videos: [video],
          sk: this.playlist.sk
        }
        const response = await this.$store.dispatch('playlists/playlistDeleteVideos', params)
      }
      catch(e) {
        console.error('Error in deleting video from playlist')
      }
      finally {
        this.deleting = false
      }
    } 
  }
}
</script>