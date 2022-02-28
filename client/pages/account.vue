<template>
  <div class="flex flex-col justify-center content-center bg-gray-200 p-10">
    <validation-observer ref="validationObservation" v-slot="{ }">
      <v-form ref="videoDescriptionForm">
        <validation-provider
          name="Description"
          rules="max:1000"
          v-slot="{ errors }"
        >
          <v-textarea
            label="About Me"
            v-model="aboutMe"
            @change="onChange"
            :error-messages="errors"
            filled
          />
          
        </validation-provider>
        <v-btn @click="onSubmitAboutMe(false)">Submit</v-btn>
      </v-form>
      
      <br>
      <v-form>
        <validation-provider
          name="Description"
          rules="max:1000"
          v-slot="{ errors }"
        >
          <v-textarea
            label="Enter your first name"
            v-model="firstName"
            @change="onChange"
            :error-messages="errors"
            filled
            rows="2"
          />
         
          
          
        </validation-provider>
        <v-btn @click="onSubmitfirstName(false)">Submit</v-btn>
      </v-form>
      
      <br>

      <v-form>
        <validation-provider
          name="Description"
          rules="max:1000"
          v-slot="{ errors }"
        >
          <v-textarea
            label="Enter your last name"
            v-model="lastName"
            @change="onChange"
            :error-messages="errors"
            filled
            rows = "2"
          />
          
        </validation-provider>
        <v-btn @click="onSubmitlastName(false)">Submit</v-btn>
      </v-form>
    </validation-observer>
  </div>

  
</template>

<script>
export default {
  layout: "dashboard",
  name: "UploadDescription",
  data() {
    return {
      // The v-model bounded description
      aboutMe: null,
      firstName: null,
      lastName: null
    };
  },
  methods: {
    onChange() {
      this.$emit("update", {
        aboutMe: this.aboutMe,
      });
    },
    
    resetaboutMe() {
      this.aboutMe = null;
    },
    async onSubmitAboutMe() {
      const aboutMe = await this.$store.dispatch("users/userPut", {
        usersAboutMe: this.aboutMe,
      });
    },
  },
  //  async onVideoSave(dialog = false) {
  //     const video = await this.$store.dispatch("videos/videosPut", {
  //       videoTitle: this.video.videoTitle,
  //       videoDescription: this.video.videoDescription,
  //       videoThumbnail: this.videoThumbnail,
  //       pk: this.video.pk,
  //       sk: this.video.sk,
  //     });
};
</script>

<style scoped></style>
