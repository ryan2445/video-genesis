<template>
  <div>
    <div class="my-52 relative">
      <div>
        <profile-banner />
      </div>
      <div class="absolute mt-0 w-full">
        
       
      </div>
    </div>
  



  <div class="flex flex-col justify-center content-center bg-gray-200 p-10">
    <validation-observer ref="validationObservation" v-slot="{}">
      <v-form ref="videoDescriptionForm">
        <validation-provider
          name="Description"
          rules="max:1000"
          v-slot="{ errors }"
        >
          <v-textarea
            
              label="Profile Picture"
              v-model="profilepicture"
            @change="onChange"
            :error-messages="errors"
            filled
            rows="2"
             />
           
           <v-textarea
            label="Enter your first name"
            v-model="firstName"
            @change="onChange"
            :error-messages="errors"
            filled
            rows="2"
          />
           <v-textarea
            label="Enter your last name"
            v-model="lastName"
            @change="onChange"
            :error-messages="errors"
            filled
            rows="2"
          />
           <v-textarea
            label="About Me"
            v-model="aboutMe"
            @change="onChange"
            :error-messages="errors"
            filled
          />
        </validation-provider>
       <v-btn @click="onSubmitAboutMe(false),onSubmitFirstName(false),onSubmitLastName(false)">Update</v-btn> 
      </v-form>
      

     
    </validation-observer>
  </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import ProfileBanner from "../components/ProfileBanner.vue";

export default {
   components: { ProfileBanner },
  layout: "dashboard",
  layout: "dashboard",
  name: "UploadDescription",
  data() {
    return {
      // The v-model bounded description
      aboutMe: null,
      firstName: null,
      lastName: null,
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
    resetfirstName() {
      this.firstName = null;
    },
    resetlastName() {
      this.lastName = null;
    },
    async onSubmitAboutMe() {
      const aboutMe = await this.$store.dispatch("users/userPut", {
        usersAboutMe: this.aboutMe,
      });
    },
    async onSubmitFirstName() {
      const firstName = await this.$store.dispatch("users/userPut", {
        usersFirstName: this.firstName,
      });
    },
    async onSubmitLastName() {
      const lastName = await this.$store.dispatch("users/userPut", {
        usersLastName: this.lastName,
      });
    },
  },
};
</script>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>

