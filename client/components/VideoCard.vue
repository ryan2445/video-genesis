<template>
  <v-card
    class="my-2 shadow-sm hover:shadow-lg overflow-hidden"
    style="
      transition: box-shadow 0.33s ease-out;
      width: 380px;
      height: 425px;
      border: 1px solid rgb(202, 202, 202);
    "
    outlined
  >
    <v-col style="padding: 0px" class="relative">
      <video-thumbnail
        :video-src="getLink(video)"
        :thumbnail-src="video.videoThumbnail || null"
        :video-key="video.videoKey"
      />
      <div class="px-2 pb-1">
        <div class="text-2xl font-medium mt-2">
          <div
            class="flex justify-between w-full items-center cursor-pointer"
            @click="onCardClick"
          >
            <div class="text-gray-800 truncate" style="height: 30px">
              {{ this.video.videoTitle }}
            </div>
            <div 
              v-if="video && isOwner"
              class="mr-2"
            >
              <video-card-settings-menu
                :video-thumbnail="videoThumbnail"
                :idx="idx"
                :video="video"
              />
            </div>
          </div>
          <v-divider class="mb-1"></v-divider>
          <div class="flex flex-row items-center">
            <v-icon small class="mr-1">icon-account-circle</v-icon>
            <div>
              <v-btn
                color="orange"
                plain
                @click="openUserPage"
                class="user-button px-0 text-left"
              >
                {{ this.owner }}
              </v-btn>
            </div>
          </div>
          <div
            class="cursor-pointer text-base whitespace-normal truncate text-gray-700"
            style="line-height: 1rem; max-height: 50px"
            @click="onCardClick"
          >
            {{ this.video.videoDescription }}
          </div>
          <v-row>
            <v-card-actions class="justify-left"></v-card-actions>
          </v-row>
        </div>
      </div>
    </v-col>
  </v-card>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      bucket_url:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
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
      return this.video.pk.substr(3);
    },
    videoThumbnail() {
      if (!this.video) return null;

      return this.video.videoThumbnail;
    },
  },
  methods: {
    openUserPage() {
      this.$router.push(`/users/username=${this.owner}`);
    },
    onCardClick() {
      this.$router.push(`/videos/pk=${this.videoPK}&sk=${this.videoSK}`);
    },
    getLink(video) {
      return `${this.bucket_url}/${video.videoKey}/${video.videoKey}_1500.mp4`;
    },
    onChange() {
      this.$emit("update", {
        // title: this.title,
        // description: video.videoDescription,
      });
    },
  },
};
</script>

<style scoped>
button.user-button >>> span.v-btn__content {
  align-items: flex-start;
}
</style>
