<template>
  <v-card style="min-width:560px;">
    <v-card-title>
      Upload video
    </v-card-title>
    <v-divider class="mt-1 mb-2 mr-2" />
    <v-card-text>
      <validation-observer ref="validationObservation" v-slot="{ invalid }">
        <v-form ref="uploadForm" @submit.prevent="handleSubmit">
          <!-- Title input -->
          <validation-provider
            name="Video title"
            rules="required|min:1|max:100"
            v-slot="{ errors }"
          >
            <v-text-field
              id="videoTitle"
              :error-messages="errors"
              label="Title"
              :success="!errors"
              v-model="videoTitle"
              color="orange lighten-1"
            >
            </v-text-field>
          </validation-provider>

          <validation-provider
            name="Video description"
            rules="max:1000"
            v-slot="{ errors }"
          >
            <v-textarea
              id="description"
              label="Description"
              :error-messages="errors"
              :success="!errors"
              v-model="videoDescription"
              color="orange lighten-1"
            >
            </v-textarea>
          </validation-provider>

          <v-checkbox
            label="make private"
            v-model="isPrivate"
            color="orange lighten-1"
          >
          </v-checkbox>

          <validation-provider
            name="fileInput"
            rules="size:500000|ext:mp3"
            v-slot="{ errors }"
          >
            <v-file-input id="fileInput" label="Upload video"
                @change="handleFileInputChange" show-size filled :error-messages="errors"
                color="orange" prepend-icon="" prepend-inner-icon="mdi-paperclip"
                :success="!errors" accept="video/mp4"
                
            />
          </validation-provider>
          
          <!-- Submit Button -->
          <div class="flex justify-center gap-x-2">
            <v-btn
              @click="handleCancel"
              class="mt-3 white--text"
              color="orange lighten-1"
            >
              Cancel
            </v-btn>
            <v-btn
              @click="handleSubmit"
              :disabled="invalid || uploading"
              :loading="uploading"
              class="mt-3 white--text"
              color="orange lighten-1"
            >
              Upload
            </v-btn>
          </div>
        </v-form>
      </validation-observer>
    </v-card-text>
  </v-card>
</template>

<script>
import { nanoid } from "nanoid";
import s3 from '../mixins/s3'
export default {
  name: "UploadVideoForm",
  mixins: [s3],
  props: {
    
  },
  data() {
    return {
      videoTitle: '',
      videoDescription: '',
      isPrivate: false,
      file: null,
      uploading: false,
      step: 1
    }
  },
  methods: {
    async handleSubmit() {
      // Indicate that we are uploading the video
      this.uploading = true;

      // Generate a key for the payload (this will be the file name)
      const key = nanoid() + '.mp4'

      // Get the input video bucket
      const bucket = "genesis2vod-staging-input-q1h5l756";

      // Upload the video to s3
      await this.s3_put(bucket, key, this.file)

      // After video is uploaded, post the video to database
      const video = await this.$store.dispatch('videos/videosPost', {
        videoTitle: this.videoTitle,
        videoDescription: this.videoDescription,
        isPrivate: this.isPrivate,
        videoKey: key
      })

      //  If the request failed, do nothing for now
      if (!video) return null

      this.$store.commit('videos/videosSet', [{...video, user: this.$store.getters['users/rootUser']}, ...this.$store.getters['videos/videos']])

      this.$emit('close')

      this.uploading = false
    },
    handleFileInputChange(file, errors) {
      console.log(file)
      console.log(errors)
      this.file = file
    },
    handleCancel() {
      this.$emit('close')
    },
    resetForm() {
      this.videoTitle = '';
      this.videoDescription = '';
      this.isPrivate = false;
      this.file = null;
    }
  }
}
</script>
