<template>
  <v-card
    class="my-2 mx-auto shadow-sm hover:shadow-lg"
    style="transition: box-shadow 0.33s ease-out; width: 380px; border: 1px solid rgb(202, 202, 202);"
    outlined
    @click="onCardClick"
  >
    <v-col style="padding:0px;">
      <VueVideoThumbnail
        :video-src="getLink(video)"
        :snapshot-at-duration-percent="70"
        :width="380"
      ></VueVideoThumbnail>
      <div class="px-2 pb-1">
        <div class="text-2xl font-medium mt-2">
          <div class="flex justify-between w-full items-center">
            <div>{{ this.video.videoTitle }}</div>
            <div class="mr-2">
              <v-menu
                v-model="showSettingsMenu"
                offset-y
                style="max-width: 480px"
                origin="top right"
                transition="scroll-y-transition"
                :nudge-left="100"
                v-if="isOwner"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-btn icon v-bind="attrs" v-on="on">
                    <v-icon>icon-cog-outline</v-icon>
                  </v-btn>
                </template>
                <v-list>
                  <v-list-item>
                    <v-dialog v-model="dialog" persistent max-width="600px">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          top
                          class="my-1"
                          color="orange"
                          dark
                          v-bind="attrs"
                          v-on="on"
                          v-ripple="{ class: 'red--text' }"
                          style="min-width:112px;"
                        >
                          <v-icon left>mdi-pencil</v-icon>EDIT
                        </v-btn>
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
                          <v-btn color="blue darken-1" text @click="onDialogClose">Close</v-btn>
                          <v-btn color="blue darken-1" text @click="onVideoSave">Save</v-btn>
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-list-item>
                  <v-list-item>
                    <v-btn
                      color="orange"
                      depressed
                      dark
                      @click.stop="onVideoDelete"
                      style="min-width:112px;"
                      class="my-1"
                    >
                      <v-icon left>mdi-delete</v-icon>Delete
                    </v-btn>
                  </v-list-item>
                </v-list>
              </v-menu>
            </div>
          </div>
          <v-divider class="mb-1"></v-divider>
          <div class="flex flex-row items-center mb-3">
            <v-icon small class="mr-1">icon-account-circle</v-icon>
            <div class="text-xs">{{ this.owner }}</div>
          </div>
          <div class="text-base text-gray-700">{{ this.video.videoDescription }}</div>
          <p v-if="!isEditing">{{ pros }}</p>
          <v-row>
            <v-card-actions class="justify-left"></v-card-actions>
          </v-row>
        </div>
      </div>
    </v-col>
  </v-card>
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
      showSettingsMenu: false
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
    isOwner() {
      return this.owner === this.user.username
    },
    owner() {
      return this.video.pk.substr(3)
    }
  },
  methods: {
    mutateVideo(param) {
      this.$store.commit("videos/videoUpdate", {
        ...param,
        idx: this.idx
      })
    },
    onCardClick() {
      this.$router.push(`videos/pk=${this.videoPK}&sk=${this.videoSK}`)
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
    }
  }
};
</script>

<style></style>
