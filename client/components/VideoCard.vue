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
              </VueVideoThumbnail>
            </nuxt-link>
          </v-col>
          <v-col cols="8">
            <v-list-item three-line>
              <v-list-item-content>
                <div class="text-3xl font-medium mt-2">
                  {{ this.video.videoTitle }}

                  <p v-if="!isEditing">
                    {{ pros }}
                  </p>
                  <v-row>
                    <v-card-actions class="justify-left">
                      <v-dialog v-model="dialog" persistent max-width="600px">
                        <template v-slot:activator="{ on, attrs }">
                          <v-btn
                            top
                            class="ma-2"
                            color="orange"
                            dark
                            v-bind="attrs"
                            v-on="on"
                            v-ripple="{ class: 'red--text' }"
                          >
                            <v-icon left> mdi-pencil </v-icon>
                            EDIT
                          </v-btn>
                          <v-card-actions class="justify-end">
                            <v-btn
                              align="right"
                              color="orange"
                              depressed
                              dark
                              @click="onVideoDelete"
                            >
                              <v-icon left> mdi-delete </v-icon>
                              Delete
                            </v-btn>
                          </v-card-actions>
                        </template>
                        <v-card>
                          <v-card-title>
                            <span class="text-h5">Edit Video Info</span>
                          </v-card-title>
                          <v-card-text>
                            <v-container>
                              <v-row>
                                <v-col cols="12">
                                  <v-text-field
                                    label="Title*"
                                    required
                                    auto-grow
                                    full-width
                                    rows="2"
                                    :value="video.videoTitle"
                                    @change="($event) => mutateVideo({ videoTitle: $event })"
                                  ></v-text-field>
                                </v-col>
                                <v-col cols="12">
                                  <v-textarea
                                    label="Description"
                                    type="text"
                                    filled
                                    :value="video.videoDescription"
                                    @change="($event) => mutateVideo({ videoDescription: $event })"
                                  />
                                </v-col>
                              </v-row>
                            </v-container>
                            <small>*indicates required field</small>
                          </v-card-text>
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
                              @click="onVideoSave"
                            >
                              Save
                            </v-btn>
                          </v-card-actions>
                        </v-card>
                      </v-dialog>
                    </v-card-actions>
                  </v-row>
                  {{ this.video.videoDescription }}
                </div>
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
import { mdiPencil, mdiDelete } from "@mdi/js";

export default {
  name: "VideoCard",
  components: { VueVideoThumbnail },
  watchQuery: ["pk", "sk"],
  data() {
    return {
      pros: "",
      isEditing: false,
      fab: false,
      top: false,
      right: false,
      dialog: false,
      bucket_url: "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
    };
  },
  props: {
    video: {
      type: Object,
      required: true,
    },
    idx: {
      type: Number,
      required: true
    }
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
  },
  methods: {
    mutateVideo(param) {
      this.$store.commit("videos/videoUpdate", {
        ...param,
        idx: this.idx
      })
    },
    async onVideoSave() {
      const video = await this.$store.dispatch("videos/videosPut", {
        videoTitle: this.video.videoTitle,
        videoDescription: this.video.videoDescription,
        pk: this.video.pk,
        sk: this.video.sk,
      });
      await this.$store.dispatch("videos/videosGet");
      this.dialog = false;
    },
    async onDialogClose() {
      this.dialog = false;
    },
    async onVideoDelete() {
      const video = await this.$store.dispatch("videos/videosDelete", {
        pk: this.video.pk,
        sk: this.video.sk,
      });
      await this.$store.dispatch("videos/videosGet");
      this.dialog = false;
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
  }
};
</script>

<style></style>
