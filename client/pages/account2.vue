<template>
  <div class="flex flex-col justify-center content-center bg-gray-200 p-10">
    <div v-if="loading" class="text-center" style="height: 100vh">
      <v-progress-circular indeterminate color="orange" style="top: 50%" />
    </div>
    <validation-observer ref="validationObservation" v-slot="{}">
      <v-form ref="videoDescriptionForm">
        <validation-provider
          name="Description"
          rules="max:1000"
          v-slot="{ errors }"
        >
          <!-- Upload Section -->
          <input
            id="file-input"
            type="file"
            name="name"
            style="display: none"
            accept=".png, .jpg, .jpeg"
            @change="profilePicSelected"
          />
          <input
            id="file-input2"
            type="file"
            name="name"
            style="display: none"
            accept=".png, .jpg, .jpeg"
            @change="coverPicSelected"
          />
          <div class="mb-4 block">
            <!-- User Profile Pic -->
            <div class="mb-4">
              <div
                v-if="userProfilePic"
                class="w-32 h-32 rounded-full overflow-hidden mb-2"
              >
                <img
                  class="min-w-full min-h-full object-cover"
                  :src="userProfilePic"
                  alt="avatar"
                />
              </div>
              <div
                v-else
                class="w-32 h-32 rounded-full overflow-hidden mb-2 bg-gray-500"
              >
                <h1 class="text-center py-12 text-xl font-bold text-white">
                  Upload
                </h1>
              </div>
              <v-btn
                :loading="loading"
                small
                color="orange lighten-1"
                class="white--text"
                @click="uploadProfilePic"
              >
                <div class="flex flex-row items-center">
                  <v-icon small class="mr-2">mdi-cloud-upload</v-icon>
                  <span
                    >{{ userProfilePic ? "Change" : "Upload" }} Profile
                    Pic</span
                  >
                </div>
              </v-btn>
            </div>
            <!-- User Cover Pic -->
            <div>
              <div v-if="userCoverPic" class="h-36 w-1/2 overflow-hidden mb-2">
                <img
                  class="min-w-full min-h-full object-cover"
                  :src="userCoverPic"
                  alt="bird"
                />
              </div>
              <div v-else class="h-36 w-1/2 overflow-hidden mb-2 bg-gray-500">
                <h1 class="text-center py-14 text-2xl font-bold text-white">
                  Upload
                </h1>
              </div>
              <v-btn
                :loading="loading"
                small
                color="orange lighten-1"
                class="white--text"
                @click="uploadCoverPic"
              >
                <div class="flex flex-row items-center">
                  <v-icon small class="mr-2">mdi-cloud-upload</v-icon>
                  <span
                    >{{ userCoverPic ? "Change" : "Upload" }} Cover Pic</span
                  >
                </div>
              </v-btn>
            </div>
          </div>
          <!-- User First Name -->
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
        <v-btn
          @click="
            onSubmitAboutMe(false),
              onSubmitFirstName(false),
              onSubmitLastName(false)
          "
          >Submit</v-btn
        >
      </v-form>
    </validation-observer>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import { nanoid } from "nanoid";
import { PutObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3";
export default {
  layout: "dashboard",
  name: "account",
  data() {
    return {
      // The v-model bounded description
      aboutMe: null,
      firstName: null,
      lastName: null,
      loading: null,
      userProfilePic: null,
      userCoverPic: null,
    };
  },
  computed: {
    ...mapGetters({
      user: "users/rootUser",
      user2: "user/user",
    }),
  },
  async mounted() {
    await this.$store.dispatch("users/userGet");
    this.loading = false;
  },

  methods: {
    onChange() {
      this.$emit("update", {
        aboutMe: this.aboutMe,
      });
    },
    uploadProfilePic() {
      document.getElementById("file-input").click();
    },
    uploadCoverPic() {
      document.getElementById("file-input2").click();
    },
    async profilePicSelected(event) {
      const file = event.target.files[0];
      const typeArr = file.type.split("/");
      this.loading = true;
      try {
        if (this.user[0].userProfilePic) {
          const urlArr = this.user[0].userProfilePic.split("/");
          const deleteKey = urlArr[urlArr.length - 1];

          const deletePayload = {
            Bucket: "videogenesis-profilepics",
            Key: deleteKey,
          };
          const deleteCommand = new DeleteObjectCommand(deletePayload);
          const deleteResp = await this.$store.getters["auth/s3"].send(
            deleteCommand
          );
        }
        const putPayload = {
          Bucket: "videogenesis-profilepics",
          Key: nanoid() + `.${typeArr[typeArr.length - 1]}`,
          Body: file,
        };

        const putCommand = new PutObjectCommand(putPayload);

        const putResp = await this.$store.getters["auth/s3"].send(putCommand);
        this.userProfilePic = `https://videogenesis-profilepics.s3.us-west-2.amazonaws.com/${putPayload.Key}`;
      } catch (error) {
        console.error(error);
      }
      this.loading = false;
      this.onSubmitUserProfilePic();
    },
    coverPicSelected() {},

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
    async onSubmitUserProfilePic() {
      console.log(this.userProfilePic);
      const userCoverPic = await this.$store.dispatch("users/userPut", {
        profilePicKey: this.userProfilePic,
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

<style scoped></style>
