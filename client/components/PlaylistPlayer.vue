<template>
  <div class="playlist-player-container">
    <v-card color="orange">
      <v-card-title>
        {{ playlist.playlistTitle }}
      </v-card-title>
      <v-card-actions>
        <v-btn @click="shuffleVideos"> shuffle </v-btn>
        <v-btn @click="onReplayPressed"> replay </v-btn>
      </v-card-actions>
      <v-list>
        <v-hover
          v-for="(playlistItem, i) in playlist.videos"
          :key="playlistItem.sk"
          v-slot="{ hover }"
        >
          <v-list-item
            @click="onPlaylistVideoClick(playlistItem.video, i)"
            class="relative cursor-pointer"
            :class="{ 'bg-gray-100': i == index, 'bg-gray-300': hover }"
          >
            <div
              class="absolute left-0 h-full flex items-center justify-center w-4"
            >
              <v-icon v-if="index == i"> icon-chevron-right </v-icon>
              <div v-else class="text-xs text-center">
                {{ i + 1 }}
              </div>
            </div>
            <v-list-item-icon>
              <video-thumbnail
                :video="playlistItem.video"
                :thumbnailSrc="playlistItem.video.videoThumbnail"
                :videoSrc="`${bucket_url}/${playlistItem.video.videoKey}/${playlistItem.video.videoKey}_1500.mp4`"
                :video-key="playlistItem.video.videoKey"
                :height="72"
                :width="128"
                class="cursor-pointer mr-2"
              />
            </v-list-item-icon>
            <v-list-item-content two-line>
              <v-list-item-title>
                {{ playlistItem.video.videoTitle }}
              </v-list-item-title>
              <v-list-item-subtitle>
                <profile-picture-and-username
                  :showPic="false"
                  text-classes="text-xs"
                  :user="playlistItem.video.user"
                />
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-hover>
      </v-list>
    </v-card>
  </div>
</template>

<script>
import { shuffle, cloneDeep } from "lodash";
export default {
  name: "PlaylistPlayer",
  props: {
    playlist: {
      type: Object,
      required: true,
    },
    // the current index we are currently playing
    index: {
      type: Number | String,
      required: true,
    },
    videosPlayList: {
      type: Array,
      required: false,
    },
    // The current video being played
    video: {
      type: Object,
      required: false
    }
  },
  data() {
    return {
      replay: false, // indicates whether the playlist will replay after watching the end of the video,
      bucket_url: "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
    };
  },
  watch: {
    videosPlayList(newVal) {
      this.videos = newVal;
    },
  },
  methods: {
    onPlaylistVideoClick(video, index) {
      this.$router.push(
        `/videos/pk=${video.pk}&sk=${video.sk}&index=${index}&list=${this.playlist.sk}`
      );
      this.$emit("video:update", video);
    },
    onReplayPressed() {
      this.$emit("replay-pressed");
    },
    shuffleVideos() {
      const videos = shuffle(cloneDeep(this.playlist.videos));

      this.$store.commit('playlists/selectedPlaylistSet', {
        ...this.playlist,
        videos
      });

      this.$emit('shuffle')
    },
  },
};
</script>

<style scoped>
.playlist-player-container {
  max-height: 580px;
}
</style>
