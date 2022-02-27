<template>
  <v-container>
    <div>
      <v-card class="mx-auto" outlined>
        <v-row>
          <v-col cols="4">
            <nuxt-link :to="`/videos/pk=${videoPK}&sk=${videoSK}`">
              <VueVideoThumbnail
                :video-src="getLink(video)"
                :snapshot-at-duration-percent="70"
                :width="500"
                :height="300"
              >
                <template #snapshot="{ snapshot }">
                  <img
                    v-if="snapshot"
                    :src="snapshot"
                    alt="https://cdn.vuetifyjs.com/images/cards/cooking.png"
                  />
                </template>
              </VueVideoThumbnail>
            </nuxt-link>
          </v-col>
          <v-col cols="8">
            <v-list-item three-line>
              <v-list-item-content>
                <v-list-item-title class="text-overline mb-4">
                  {{ video.videoTitle }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ video.videoDescription }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-col>
        </v-row>
      </v-card>
      <br />
    </div>
  </v-container>
</template>

<script>
import VueVideoThumbnail from "vue-video-thumbnail";
import { mapGetters } from "vuex";
export default {
  components: { VueVideoThumbnail },
  watchQuery: ["pk", "sk"],
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
  },
  methods: {
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
  watchQuery(newQuery, oldQuery) {
    console.log("watchQuery");
    console.log(newQuery);
    // Only execute component methods if the old query string contained `bar`
    // and the new query string contains `foo`
    return newQuery.foo && oldQuery.bar;
  },
};
</script>

<style></style>
