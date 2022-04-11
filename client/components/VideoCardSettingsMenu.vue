<template>
  <v-menu
    v-model="display"
    offset-y
    origin="top right"
    transition="scroll-y-transition"
    :nudge-left="100"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn icon v-bind="attrs" v-on="on">
        <v-icon>icon-cog-outline</v-icon>
      </v-btn>
    </template>
    <div style="max-width: 480px; background: white">
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
                style="min-width: 112px"
              >
                <v-icon left>mdi-pencil</v-icon>
                <span>Edit</span>
              </v-btn>
            </template>
            <v-card class="overflow-x-hidden">
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
                    <v-col v-if="video.videoThumbnail" cols="12">
                      <div>Video Thumbnail:</div>
                    </v-col>
                    <v-col v-if="video.videoThumbnail" cols="12">
                      <img :src="video.videoThumbnail" width="300px" />
                    </v-col>
                    <v-col cols="12">
                      <div class="flex flex-col">
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
                              <span>
                                {{ video.videoThumbnail ? "Change" : "Upload" }}
                                Thumbnail
                              </span>
                            </div>
                          </v-btn>
                        </div>
                        <div>
                            <br />
                          <v-select
                            :value="undefined"
                            @change="onDefaultThumbnailChange"
        
                            v-if="altThumbnails"
                            :items="
                              altThumbnails.map(
                                (item) =>
                                  'https://videogenesis-thumbnails.s3.us-west-2.amazonaws.com/' +
                                  video.videoKey +
                                  '/' +
                                  item
                              )
                            "
                            label="Choose a default thumbnail"
                          >
                            <template v-slot:item="{ item }">
                              <div style="width: 30vw">
                                <img :src="item" />
                                <br />
                              </div>
                            </template>
                          </v-select>
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
                            mutateVideo({
                              videoTitle: $event,
                            })
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
                            mutateVideo({
                              videoDescription: $event,
                            })
                        "
                      />
                    </v-col>
                  </v-row>
                </v-container>
                <small>*indicates required field</small>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="onDialogClose"
                  >Close</v-btn
                >
                <v-btn color="blue darken-1" text @click="onVideoSave(false)"
                  >Save</v-btn
                >
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-list-item>
        <v-list-item>
          <v-dialog v-model="deleteDialogBox" max-width="600px">
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
                <v-icon left>mdi-delete</v-icon>
                <span>Delete</span>
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
                  >Cancel</v-btn
                >

                <v-btn
                  class="mx-auto transition-swing secondary"
                  elevation="12"
                  height="25"
                  width="1%"
                  color="orange"
                  plain
                  @click.stop="onVideoDelete"
                  >Delete</v-btn
                >
              </v-sheet>
            </div>
          </v-dialog>
        </v-list-item>
      </v-list>
    </div>
  </v-menu>
</template>

<script>
import s3 from "../mixins/s3";
import {cloneDeep} from "lodash"; 
export default {
  name: "VideoCardSettingsMenu",
  mixins: [s3],
  props: {
    idx: {
      type: Number,
      required: true,
    },
    video: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      display: false,
      dialog: false,
      loading: false,
      defaultVideoThumbnail: this.video.videoThumbnail,
      altThumbnails: this.video.altThumbnails, 
      deleteDialogBox: false,
    };
  },
  methods: {
    uploadThumbnail() {
      document.getElementById("file-input").click();
    },
    async thumbnailSelected(event) {
      // Find the selected file
      const file = event.target?.files[0];

      // If the file does not exist, return
      if (!file) return;

      // Indicate that we are loading
      this.loading = true;

      // Get the bucket for video thumbnails
      const bucket = "videogenesis-thumbnails";

      // If there is an existing thumbnail, delete it
      if (this.video.videoThumbnail) {
        const delete_key = this.key_from_string(this.video.videoThumbnail);

        await this.s3_delete(bucket, delete_key);
      }

      // Construct a unique key from the file
      const put_key = this.key_from_file(file);

      // Upload the thumbnail
      const thumbnail_url = await this.s3_put(bucket, put_key, file);

      // Update the local thumbnail url
      this.defaultVideoThumbnail = thumbnail_url;

      this.$store.commit("videos/videoUpdate", {
        ...this.video,
        videoThumbnail: thumbnail_url,
      });

      // re-query the updated videos
      await this.onVideoSave(true);

      // Indicate that we are done loading
      this.loading = false;
    },
    async onVideoSave(dialog = false) {
      await this.$store.dispatch("videos/videosPut", {
        videoTitle: this.video.videoTitle,
        videoDescription: this.video.videoDescription,
        videoThumbnail: this.defaultVideoThumbnail || this.video.videoThumbnail,
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
    onDefaultThumbnailChange(defaultVideoThumbnail)
    {
        this.defaultVideoThumbnail = defaultVideoThumbnail; 
        let altThumbnails = cloneDeep(this.altThumbnails); 
        new Promise 
        (
            (resolve, reject) => 
            {
                this.altThumbnails = undefined; 
                console.log(altThumbnails); 
                resolve(); 
            }
        ).then(()=>this.altThumbnails = altThumbnails); 
    },
    async onDialogClose() {
      this.dialog = false;
    },
    async onDeleteDialogClose() {
      this.deleteDialogBox = false;
    },
    async onVideoDelete() {
      await this.$store.dispatch("videos/videosDelete", {
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
    mutateVideo(param) {
      this.$store.commit("videos/videoUpdate", {
        ...param,
        idx: this.idx,
      });
    },
  },
};
</script>
