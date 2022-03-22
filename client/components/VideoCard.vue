<template>
  <div>
    <v-hover v-show="loaded" v-slot="{ hover }" :open-delay="300">
      <v-card
        class="video-card my-2 shadow-sm hover:shadow-lg overflow-hidden z-30"
        style="
          width: 380px;
          height: 425px;
          border: 1px solid rgb(202, 202, 202);
        "
        :class="{'card-hover' : hover}"
        outlined
      >
        <v-col style="padding: 0px" class="relative">
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
                <div 
                  v-if="video && isOwner"
                  class="mr-2"
                >
                  <v-hover>
                    <video-card-settings-menu
                      :video-thumbnail="videoThumbnail"
                      :idx="idx"
                      :video="video"
                    />
                  </v-hover>
                </div>
              </div>
              <v-divider class="mb-1"></v-divider>
              <div class="flex flex-row items-center">
                <div
                  v-if="video.user && !!video.user.profilePicKey"
                  @click="openUserPage"
                  style="width:36px; height:36px;"
                  class="mr-1"
                >
                  <img
                    :src="video.user.profilePicKey"
                    :alt="video.user.username"
                    class="rounded-full w-full h-full object-cover cursor-pointer"
                  />
                </div>
                <v-icon v-else large class="mr-1" @click="openUserPage">icon-account-circle</v-icon>
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
              <div
                class="py-1 overflow-hidden"
                style="max-height: 49px;"
              >
                <div
                  class="cardDescription text-gray-700"
                >
                  {{ video.videoDescription }}
                </div>
              </div>
              <v-row>
                <v-card-actions class="justify-left"></v-card-actions>
              </v-row>
            </div>
          </div>
        </v-col>
      </v-card>
    </v-hover>
    <v-skeleton-loader
      v-show="!loaded"
      class="mx-auto"
      :width="380"
      :height="425"
      type="image, card-heading, list-item-avatar, list-item-two-line"
    >

    </v-skeleton-loader>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      bucket_url: "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",

      startTime: 0,

      thumbnailLoaded: false
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
  },
  mounted() {
  },
  computed: {
    ...mapGetters({
      user: "user/user",
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
      if (!this.video) return null
      if (!this.video.pk) return null
      return this.video.pk.substr(3);
    },
    videoThumbnail() {
      if (!this.video) return null;

      return this.video.videoThumbnail;
    },
    loaded() {
      return this.thumbnailLoaded
    }
  },
  methods: {
    openUserPage() {
      this.$router.push(`/users/username=${this.owner}`);
    },
    onCardClick() {
      this.$router.push(`/videos/pk=${this.videoPK}&sk=${this.videoSK}&time=${this.startTime}`);
    },
    getLink(video) {
      return `${this.bucket_url}/${video.videoKey}/${video.videoKey}_1500.mp4`;
    },
    onVideoTimeChange(newTime) {
      this.startTime = newTime
    },
    onThumbnailLoaded() {
      this.thumbnailLoaded = true
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

.cardTitle, .cardDescription {
  line-height: 1;
  display: -webkit-box;
  -webkit-box-orient: vertical;
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
