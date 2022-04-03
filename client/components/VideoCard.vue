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
        <super-resolution-banner v-if="superResEnabled" />
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
          <div class="text-2xl font-medium mt-2">
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
                    <v-icon>playlist_add</v-icon>
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
                            @click="createNewPlaylist(video.sk)"
                          >
                            Create
                          </v-btn>
                        </v-card-actions>
                        <!-- <v-layout row wrap>
                          <v-flex
                            v-for="(title, index) in playlist"
                            :key="playlist[index].playlistTitle"
                            xs6
                          >
                            <v-checkbox
                              light
                              :label="title.playlistTitle"
                              @click="
                                addVideoToPlaylist(title.sk, title.videos)
                              "
                            >
                              
                            </v-checkbox>
                          </v-flex>
                        </v-layout> -->
                        <form @submit.prevent="handleSubmit">
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
                              v-model="user.namesOfThePlaylists"
                              :id="item.playlistTitle"
                              :value="item"
                            />
                          </div>
                          <!-- print result -->
                          <!-- <div class="form-group">
                            {{ user.namesOfThePlaylists }}
                          </div> -->
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
    <v-skeleton-loader
      v-show="!loaded"
      class="mx-auto opacity-80"
      :width="380"
      :height="425"
      type="image, card-heading, list-item-avatar, list-item-two-line"
    >
    </v-skeleton-loader>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import "material-design-icons-iconfont/dist/material-design-icons.css"; // Ensure you are using css-loader
import Vue from "vue";
import Vuetify from "vuetify/lib";

Vue.use(Vuetify);

export default {
  icons: {
    iconfont: "md",
  },

  data() {
    return {
      user: {
        namesOfThePlaylists: [],
      },
      loading: false,
      dialog: false,
      playlistsDialogBox: false,
      bucket_url:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",

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
    },
    playlist: {
      type: Object,
      required: true,
    },
  },
  mounted() {},
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
    async handleSubmit() {
      for (let index = 0; index < this.playlist.length; index++) {
        if (String(this.playlist[index].videos).includes(this.video.sk)) {
          var deleteVideoFromPlaylist = true;
          for (let i = 0; i < this.user.namesOfThePlaylists.length; i++) {
            if (this.playlist[index] === this.user.namesOfThePlaylists[i]) {
              deleteVideoFromPlaylist = false;
            }
          }

          if (deleteVideoFromPlaylist) {
            // alert("remove video from");
            // alert(this.playlist[index].playlistTitle);
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
        index < this.user.namesOfThePlaylists.length;
        index++
      ) {
        await this.addVideoToPlaylist(
          this.user.namesOfThePlaylists[index].sk,
          this.user.namesOfThePlaylists[index].videos
        );
      }
    },
    async onDialogClose() {
      this.playlistsDialogBox = false;
    },
    async createNewPlaylist(videoKey) {
      //  Create playlist
      await this.$store.dispatch("playlists/playlistsPost", {
        playlistTitle: this.newPlayListName,
        isPrivate: this.isPrivate,
        videos: videoKey,
      });
      this.playlistsDialogBox = false;
    },
    async UpdatePlaylist(videoSk) {
      // alert(videoSk);
      // alert(this.owner);
      const playlistNames = await this.$store.dispatch(
        "playlists/playlistsGet"
      );

      // console.log(this.playlist);
      for (let index = 0; index < this.playlist.length; index++) {
        // alert(this.playlist[index].videos);
        // alert(String(this.playlist[index].videos).includes(videoSk));
        if (String(this.playlist[index].videos).includes(videoSk)) {
          this.user.namesOfThePlaylists.push(this.playlist[index]);
        }
      }
      // var videoPlaylistInfo = await this.$store.dispatch(
      //   "playlists/getPlaylistsByVideo",
      //   {
      //     username: this.owner,
      //     video: videoSk,
      //   }
      // );

      // console.log(videoPlaylistInfo);
    },
    async addVideoToPlaylist(playlistKey, videos) {
      // alert(this.video.sk);
      // alert(playlistKey);
      const playlistNames = await this.$store.dispatch(
        "playlists/playlistsPut",
        {
          sk: playlistKey,
          videos: videos + "," + this.video.sk,
        }
      );
      // console.log("playlistNames: ");
      // console.log(this.playlist);
    },
    async removeVideoFromPlaylist(playlistKey, videos, videoToRemove) {
      // alert("video to remove:    " + videoToRemove);
      // alert(videos);
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
      // console.log("playlistNames: ");
      // console.log(this.playlist);
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
