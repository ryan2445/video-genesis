<template>
  <v-card
    class="my-2 mx-auto shadow-sm hover:shadow-lg"
    style="
      transition: box-shadow 0.33s ease-out;
      width: 380px;
      height: 425px;
      border: 1px solid rgb(202, 202, 202);
    "
    outlined
    @click="onCardClick"
  >
    <v-col style="padding: 0px" class="relative">
      <div
        style="width: 380px; height: 250px"
        class="flex justify-center items-center bg-black"
        v-if="!thumbnailReady"
      >
        <v-progress-circular indeterminate color="orange" />
      </div>
      <VueVideoThumbnail
        :style="{
          opacity: thumbnailReady ? '1' : '0',
        }"
        :video-src="getLink(video)"
        :snapshot-at-duration-percent="70"
        :width="380"
        @snapshotCreated="onSnapshotCreated"
      >
        <template #snapshot="{ snapshot }">
          <img
          v-if="snapshot"
          :src="video.videoThumbnail || snapshot"
          alt="snapshot"
          :width="380"
          :height="280"
          style="object-fit:contain;"
          >
        </template>
      </VueVideoThumbnail>
      <div class="px-2 pb-1">
        <div class="text-2xl font-medium mt-2">
          <div class="flex justify-between w-full items-center">
            <div v-if="this.video.videoTitle.length < 25">
              {{ this.video.videoTitle }}
            </div>
            <div v-else>
              {{ this.video.videoTitle.substring(0, 25) + "..." }}
            </div>
            <!-- <div>{{ this.video.videoTitle }}</div> -->
            <div class="mr-2">
              <v-menu
                v-model="showSettingsMenu"
                offset-y
                style="max-width: 480px"
                class="z-30"
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
                <v-list class="z-30">
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
                          style="min-width: 112px"
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
                              <!-- Invisible file input menu - only opens when user clicks upload thumbnail -->
                              <input
                                id="file-input"
                                type="file"
                                name="name"
                                style="display: none"
                                accept=".png, .jpg, .jpeg"
                                @change="thumbnailSelected"
                              />
                              <v-col v-if="videoThumbnail" cols="12">
                                <div>Video Thumbnail:</div>
                              </v-col>
                              <v-col v-if="videoThumbnail" cols="12">
                                <img :src="videoThumbnail" width="300px" />
                              </v-col>
                              <v-col cols="12">
                                <div class="flex flex-row">
                                  <div>
                                    <v-btn
                                      :loading="loading"
                                      small
                                      color="orange lighten-1"
                                      class="white--text"
                                      @click="uploadThumbnail"
                                    >
                                      <div class="flex flex-row items-center">
                                        <v-icon small class="mr-2"
                                          >mdi-cloud-upload</v-icon
                                        >
                                        <span
                                          >{{
                                            videoThumbnail ? "Change" : "Upload"
                                          }}
                                          Thumbnail</span
                                        >
                                      </div>
                                    </v-btn>
                                  </div>
                                </div>
                              </v-col>
                              <v-col cols="12">
                                <v-text-field
                                  label="Title*"
                                  required
                                  auto-grow
                                  full-width
                                  rows="2"
                                  :value="video.videoTitle"
                                  @change="
                                    ($event) =>
                                      mutateVideo({ videoTitle: $event })
                                  "
                                ></v-text-field>
                              </v-col>
                              <v-col cols="12">
                                <v-textarea
                                  label="Description"
                                  type="text"
                                  filled
                                  :value="video.videoDescription"
                                  @change="
                                    ($event) =>
                                      mutateVideo({ videoDescription: $event })
                                  "
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
                            >Close</v-btn
                          >
                          <v-btn
                            color="blue darken-1"
                            text
                            @click="onVideoSave(false)"
                            >Save</v-btn
                          >
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                  </v-list-item>
                </v-list>
                <v-list-item>
                  <template>
                    <v-dialog v-model="deleteDialogBox" width="335">
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn
                          top
                          class="my-1"
                          color="orange"
                          dark
                          v-bind="attrs"
                          v-on="on"
                          v-ripple="{ class: 'red--text' }"
                          style="min-width: 112px"
                        >
                          <v-icon left>mdi-delete</v-icon>DELETE
                        </v-btn>
                      </template>
                      <div class="text-center">
                        <v-sheet
                          class="px-7 pt-7 pb-4 mx-auto text-center d-inline-block"
                          color="white"
                          dark
                        >
                          <div class="orange pa-4 bg-secondary rounded-t-xl">
                            Are you sure you want to delete this video?
                          </div>

                          <v-btn
                            class="ma-1"
                            elevation="12"
                            height="25"
                            width="1%"
                            color="orange"
                            plain
                            @click.stop="onDeleteDialogClose"
                          >
                            Cancel
                          </v-btn>

                          <v-btn
                            class="mx-auto transition-swing secondary"
                            elevation="12"
                            height="25"
                            width="1%"
                            color="orange"
                            plain
                            @click.stop="onVideoDelete"
                          >
                            Delete
                          </v-btn>
                        </v-sheet>
                      </div>
                    </v-dialog>
                  </template>
                </v-list-item>
              </v-menu>
            </div>
          </div>
          <v-divider class="mb-1"></v-divider>
          <div class="flex flex-row items-center mb-3">
            <v-icon small class="mr-1">icon-account-circle</v-icon>
            <template>
              <div>
                <v-btn
                  class="ma-2"
                  width="15%"
                  color="orange"
                  plain
                  @click="openUserPage"
                >
                  {{ this.owner }}
                </v-btn>
              </div>
            </template>
          </div>
          <div class="text-base text-gray-700">
            {{ video.videoDescription }}
          </div>
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
import { nanoid } from "nanoid";
import { PutObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3";
export default {
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
      deleteDialogBox: false,
      bucket_url:
        "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
      showSettingsMenu: false,
      thumbnailReady: false,
      thumbnail: null,
      loading: null,
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

  mounted() {},
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

      return this.thumbnail || this.video.videoThumbnail;
    },
  },
  methods: {
    onSnapshotCreated() {
      this.thumbnailReady = true;
    },
    uploadThumbnail() {
      document.getElementById("file-input").click();
    },
    async thumbnailSelected(event) {
      const file = event.target.files[0];

      const typeArr = file.type.split("/");

      this.loading = true;

      try {
        //  Delete old thumbnail
        if (this.video.videoThumbnail) {
          const urlArr = this.video.videoThumbnail.split("/");

          const deleteKey = urlArr[urlArr.length - 1];

          const deletePayload = {
            Bucket: "videogenesis-thumbnails",
            Key: deleteKey,
          };

          const deleteCommand = new DeleteObjectCommand(deletePayload);

          const deleteResp = await this.$s3.send(deleteCommand);
        }

        const putPayload = {
          Bucket: "videogenesis-thumbnails",
          Key: nanoid() + `.${typeArr[typeArr.length - 1]}`,
          Body: file,
        };

        const putCommand = new PutObjectCommand(putPayload);

        const putResp = await this.$s3.send(putCommand);

        this.thumbnail = `https://videogenesis-thumbnails.s3.us-west-2.amazonaws.com/${putPayload.Key}`;
      } catch (error) {
        console.error(error);
      }

      this.loading = false;

      this.onVideoSave(true);
    },
    openUserPage() {},
    mutateVideo(param) {
      this.$store.commit("videos/videoUpdate", {
        ...param,
        idx: this.idx,
      });
    },
    onCardClick() {
      this.$router.push(`videos/pk=${this.videoPK}&sk=${this.videoSK}`);
    },
    async onVideoSave(dialog = false) {
      const video = await this.$store.dispatch("videos/videosPut", {
        videoTitle: this.video.videoTitle,
        videoDescription: this.video.videoDescription,
        videoThumbnail: this.videoThumbnail,
        pk: this.video.pk,
        sk: this.video.sk,
      });

      // If on the 'Explore' page get every user's video or get the user's videos
      await this.$store.dispatch(
        this.$router.history.current.name === "Explore"
          ? "videos/getAllVideos"
          : "videos/videosGet"
      );

      this.dialog = dialog;
    },
    async onDialogClose() {
      this.dialog = false;
    },
    async onDeleteDialogClose() {
      this.deleteDialogBox = false;
    },
    async onVideoDelete() {
      const video = await this.$store.dispatch("videos/videosDelete", {
        pk: this.video.pk,
        sk: this.video.sk,
      });

      // If on the 'Explore' page get every user's video or get the user's videos
      await this.$store.dispatch(
        this.$router.history.current.name === "Explore"
          ? "videos/getAllVideos"
          : "videos/videosGet"
      );

      this.deleteDialogBox = false;
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

<style></style>
