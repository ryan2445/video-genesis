<template>
    <v-card rounded width="600">
        <v-stepper v-model="step">
            <v-stepper-items>
                <v-stepper-content step="1">
                    <v-card-title class="bg-gray-300">
                        <div class="flex justify-center">
                            <h3>Upload Video</h3>
                            <v-icon right> icon-video </v-icon>
                        </div>
                    </v-card-title>
                    <upload-description ref="uploadDescription"
                        @update="onVideoDescriptionUpdate" />
                    <upload-box ref="uploadBox" @update="onVideoUpdate" />
                    <div class="flex flex-grow justify-center bg-gray-300 py-3">
                        <v-btn @click="onUpload" :loading="uploading"
                            :disabled="uploading" color="orange" class="white--text">
                            Upload
                        </v-btn>
                    </div>
                </v-stepper-content>
                <v-stepper-content step="2">
                    <v-card-title class="bg-gray-300" style="display: block">
                        <div class="flex justify-center">
                            <v-icon left color="green"> icon-check-circle </v-icon>
                            <h3>Video Upload Success!</h3>
                        </div>
                        <div class="flex justify-center pt-8">
                            <v-btn @click="resetVideoForm()" color="orange"
                                class="white--text">
                                <v-icon class="mr-2"> mdi-file-video </v-icon>
                                Upload Another Video
                            </v-btn>
                        </div>
                        <div class="flex justify-center pt-8">
                            <v-btn @click="resetVideoForm(), $router.push('/videos')"
                                color="orange" class="white--text">
                                <v-icon class="mr-2"> mdi-format-list-text </v-icon>
                                View Videos
                            </v-btn>
                        </div>
                    </v-card-title>
                </v-stepper-content>
            </v-stepper-items>
        </v-stepper>
    </v-card>
</template>

<script lang="js">
import { nanoid } from "nanoid";
import s3 from '../mixins/s3'
export default {
    name: "VideoForm",
    mixins: [s3],
    data() {
      return {
          // The title of the video
          title: null,
          // The description of the video
          description: null,
          isPrivate: false,
          // The video
          video: null,
          // Determines if we are currently uploading
          uploading: false,
          //  Shows if a video has been successfully uploaded
          uploaded: false,
          //  Step number for the v-stepper
          step: 1
      }
    },
    methods: {
      onVideoDescriptionUpdate(object) {

        this.title = object.title
        this.description = object.description
        this.isPrivate = object.isPrivate
        console.log("onvideodes", object.isPrivate, this.isPrivate)
      },
      async onUpload() {
        // If the video was not set, alert the user
        if (!this.video) {
          alert("Select a video before uploading");
          return;
        } else if (this.video.type !== "video/mp4") {
          alert("Only mp4 files are supported");
          return;
        } else if (this.video.size > 5.12e8) {
          alert("The file size must be less than 512MB");
          return;
        }

        // Indicate that we are uploading the video
        this.uploading = true;

        // Generate a key for the payload (this will be the file name)
        const key = nanoid() + '.mp4'

        // Get the input video bucket
        const bucket = "genesis2vod-staging-input-q1h5l756";

        // Upload the video to s3
        await this.s3_put(bucket, key, this.video)

        // After video is uploaded, post the video to database
        const video = await this.$store.dispatch('videos/videosPost', {
            videoTitle: this.title,
            videoDescription: this.description,
            isPrivate: this.isPrivate,
            videoKey: key
        })

        //  If the request failed, do nothing for now
        if (!video) return null

        //  Go to confirmation step
        this.step = 2

        // Generate the payload
        const payload = {
          Bucket: "genesis2vod-staging-input-q1h5l756",
          Key: key,
          Body: this.video,
        };

        this.uploading = false;
      },
      onVideoUpdate(video) {
          this.video = video
      },
      resetVideoForm() {
          this.$refs.uploadBox.resetUploadBox()
          this.$refs.uploadDescription.resetUploadDescritpion()
          this.title = null
          this.description = null
          this.video = null
          this.step = 1
      }
    }
}
</script>
<style scoped>
.v-stepper__content {
    padding: 0px;
}
</style>
