<template>
  <div>
    <v-hover v-show="loaded" v-slot="{ hover }" :open-delay="500">
      <v-card
        class="video-card my-2 shadow-sm hover:shadow-lg relative overflow-hidden"
        style="
          max-width: 380px;
          height: 425px;
          border: 1px solid rgb(202, 202, 202);
        "
        :class="{ 'card-hover': hover }"
        outlined
      >
        <super-resolution-banner 
          v-if="superResEnabled" 
        />
        <video-thumbnail
          class="cursor-pointer"
          :video-src="getLink(video)"
          :thumbnail-src="video.videoThumbnail || null"
          :video-key="video.videoKey"
          :play="hover"
          @click="onCardClick"
          @videoTimeChange="onVideoTimeChange"
          @thumbnail:loaded="onThumbnailLoaded"
        />
        <div class="px-2 pb-1">
          <div class="mt-2">
            <div
              class="flex justify-between w-full items-center cursor-pointer"
              @click="onCardClick"
            >
              <div class="text-gray-800 cardTitle">
                {{ video.videoTitle }}
              </div>
              <div v-if="video && isOwner" class="mr-2">
                <v-hover>
                  <video-card-settings-menu
                    :video-thumbnail="videoThumbnail"
                    :idx="idx"
                    :video="video"
                    :playlist="playlist"
                  />
                </v-hover>
              </div>
            </div>
            <v-divider class="mb-1"></v-divider>
            <div class="flex flex-row items-center">
              <div
                v-if="video.user && !!video.user.profilePicKey"
                @click="openUserPage"
                style="width: 36px; height: 36px"
                class="mr-1"
              >
                <img
                  :src="video.user.profilePicKey"
                  :alt="video.user.username"
                  class="rounded-full w-full h-full object-cover cursor-pointer"
                />
              </div>
              <v-icon v-else large class="mr-1" @click="openUserPage"
                >icon-account-circle</v-icon
              >
              <div>
                <v-btn
                  color="orange"
                  plain
                  @click="openUserPage"
                  class="user-button px-0 text-left"
                >
                  {{ owner }}
                </v-btn>
              </div>
            </div>
            <div class="mr-3">
              <v-dialog
                v-model="playlistsDialogBox"
                persistent
                max-width="600px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    v-bind="attrs"
                    v-on="on"
                    fab
                    depressed
                    color="grey lighten-1"
                    width="30"
                    height="30"
                    class="mb-2 shadow-md justify-right"
                    @click="UpdatePlaylist(video.sk)"
                  >
                    <v-icon>icon-playlist-plus</v-icon>
                  </v-btn>
                </template>
                <v-card>
                  <v-card-title>
                    <span class="text-h5"> Playlist </span>
                  </v-card-title>
                  <v-card-text>
                    <v-container>
                      <v-row>
                        <v-col cols="12">
                          <v-text-field
                            label="Create a new playlist"
                            type="text"
                            filled
                            v-model="newPlayListName"
                          />
                        </v-col>
                      </v-row>
                      <v-container fluid>
                        <v-checkbox
                          v-model="isPrivate"
                          label="Make the Playlist Private"
                          @change="onChange"
                        ></v-checkbox>

                        <v-card-actions>
                          <v-spacer></v-spacer>
                          <v-btn
                            color="blue darken-1"
                            text
                            @click="onDialogClose"
                          >
                            Close
                          </v-btn>
                          <v-btn
                            color="blue darken-1"
                            text
                            @click="createNewPlaylist(video)"
                          >
                            Create
                          </v-btn>
                        </v-card-actions>

                        <form @submit.prevent="handlePlaylistSubmit" class="playlist-form">
                          <div
                            class="form-group form-check"
                            v-for="item in playlist"
                            v-bind:key="item.id"
                          >
                            <label class="form-check-label" :for="item.id">{{
                              item.playlistTitle
                            }}</label>
                            <input
                              type="checkbox"
                              v-model="namesOfThePlaylists"
                              :id="item.playlistTitle"
                              :value="item"
                            />
                          </div>

                          <div class="form-group">
                            <button class="btn btn-primary">Submit</button>
                          </div>
                        </form>
                      </v-container>
                    </v-container>
                  </v-card-text>
                </v-card>
              </v-dialog>
            </div>
            <div class="py-1 overflow-hidden" style="max-height: 49px">
              <div class="cardDescription text-gray-700">
                {{ video.videoDescription }}
              </div>
            </div>
            <v-row>
              <v-card-actions class="justify-left"></v-card-actions>
            </v-row>
          </div>
        </div>
      </v-card>
    </v-hover>

    <!-- While the video is still loading, show the skeleton-loader -->
    <v-skeleton-loader
      v-show="!loaded"
      class="mx-auto opacity-80"
      :width="380"
      :height="425"
      type="image, card-heading, list-item-avatar, list-item-two-line"
    />
  </div>
</template>
<script>
import { mapGetters } from "vuex";

export default {
  name: "VideoCard",
  data() {
    return {
      namesOfThePlaylists: [],
      loading: false,
      dialog: false,
      playlistsDialogBox: false,
      bucket_url: "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      startTime: 0,
      thumbnailLoaded: false,
      newPlayListName: null,
      isPrivate: false,
      playlistNames: {
        addToPlaylist: [],
      },
    };
  },
  props: {
    video: {
      type: Object,
      required: true,
    },
    idx: {
      type: Number,
      required: true,
    }
  },
  computed: {
    ...mapGetters({
      user: "user/user",
      playlist: "playlists/playlists",
    }),
    videoPK() {
      // If the video does not exist, return null
      if (!this.video) return null;

      return this.video.pk;
    },
    videoSK() {
      // If the video does not exist, return null
      if (!this.video) return null;

      return this.video.sk;
    },
    isOwner() {
      return this.owner === this.user.username;
    },
    owner() {
      if (!this.video) return null;
      if (!this.video.pk) return null;
      return this.video.pk.substr(3);
    },
    videoThumbnail() {
      if (!this.video) return null;

      return this.video.videoThumbnail;
    },
    loaded() {
      return this.thumbnailLoaded;
    },
    superResEnabled() {
      return !!this.video && !!this.video.lrBaseURL && !!this.video.hrBaseURL;
    },
  },
  methods: {
    async handlePlaylistSubmit() {
      for (let index = 0; index < this.playlist.length; index++) {
        if (String(this.playlist[index].videos).includes(this.video.sk)) {
          let deleteVideoFromPlaylist = true;

          for (let i = 0; i < this.namesOfThePlaylists.length; i++) {
            if (this.playlist[index] === this.namesOfThePlaylists[i]) {
              deleteVideoFromPlaylist = false;
            }
          }

          if (deleteVideoFromPlaylist) {
            await this.removeVideoFromPlaylist(
              this.playlist[index].sk,
              this.playlist[index].videos,
              this.video.sk
            );
          }
        }
      }

      for (
        let index = 0;
        index < this.namesOfThePlaylists.length;
        index++
      ) {
        await this.addVideoToPlaylist(
          this.namesOfThePlaylists[index].sk,
          this.namesOfThePlaylists[index].videos
        );
      }
    },
    async onDialogClose() {
      this.playlistsDialogBox = false;
    },
    async createNewPlaylist(video) {
      //  Create playlist
      await this.$store.dispatch("playlists/playlistsPost", {
        playlistTitle: this.newPlayListName,
        isPrivate: this.isPrivate,
        video: video,
      });
      this.playlistsDialogBox = false;
    },
    async UpdatePlaylist(videoSk) {
      const playlistNames = await this.$store.dispatch(
        "playlists/playlistsGet"
      );

      for (let index = 0; index < this.playlist.length; index++) {
        if (String(this.playlist[index].videos).includes(videoSk)) {
          this.namesOfThePlaylists.push(this.playlist[index]);
        }
      }
    },
    async addVideoToPlaylist(playlistKey, videos) {
      const playlistNames = await this.$store.dispatch(
        "playlists/playlistsPut",
        {
          sk: playlistKey,
          videos: videos + "," + this.video.sk,
        }
      );
    },
    async removeVideoFromPlaylist(playlistKey, videos, videoToRemove) {
      videos = String(videos).replace(videoToRemove + ",", "");
      videos = String(videos).replace(",,", "");
      videos = String(videos).replace("," + videoToRemove, "");
      videos = String(videos).replace(videoToRemove, "");
      // alert(videos);
      const playlistNames = await this.$store.dispatch(
        "playlists/playlistsPut",
        {
          sk: playlistKey,
          videos: videos,
        }
      );
    },
    onChange() {
      this.$emit("update", {
        isPrivate: this.isPrivate,
      });
    },
    openUserPage() {
      this.$router.push(`/users/username=${this.owner}`);
    },
    onCardClick() {
      this.$router.push(
        `/videos/pk=${this.videoPK}&sk=${this.videoSK}&time=${this.startTime}`
      );
    },
    getLink(video) {
      return `${this.bucket_url}/${video.videoKey}/${video.videoKey}_1500.mp4`;
    },
    onVideoTimeChange(newTime) {
      this.startTime = newTime;
    },
    onThumbnailLoaded() {
      this.thumbnailLoaded = true;
    },
  },
};
</script>

<style scoped>
button.user-button >>> span.v-btn__content {
  align-items: flex-start;
}
.video-card {
  transition: transform linear 0.2s, box-shadow linear 0.3s;
}
.card-hover {
  z-index: 40;
  transform: scale(1.15);
}

.cardTitle,
.cardDescription {
  line-height: 1;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.cardTitle {
  max-height: 33px;
  font-size: 16px;
  -webkit-line-clamp: 2;
}

.cardDescription {
  max-height: 42px;
  font-size: 14px;
  -webkit-line-clamp: 3;
  padding: 2px 0;
}
</style>
