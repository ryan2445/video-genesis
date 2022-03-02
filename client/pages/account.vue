<template>
  <div>
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

    <!-- User Profile Pic -->

    <div class="mb-4 my-4">
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
        <h1 class="text-center py-12 text-xl font-bold text-white">Upload</h1>
      </div>
      <v-btn
        :loading="loadingProfilePic"
        small
        color="orange lighten-1"
        class="white--text"
        @click="uploadProfilePic"
      >
        <div class="flex flex-row items-center">
          <v-icon small class="mr-2">mdi-cloud-upload</v-icon>
          <span>{{ userProfilePic ? "Change" : "Upload" }} Profile Pic</span>
        </div>
      </v-btn>
    </div>
    <!-- User Cover Pic -->
    <div class="mb-4">
      <div
        v-if="userCoverPic"
        class="h-36 w-1/2 overflow-hidden mb-2 bg-gray-500"
      >
        <img
          class="min-w-full min-h-full object-cover"
          :src="userCoverPic"
          alt="bird"
        />
      </div>
      <div v-else class="h-36 w-1/2 overflow-hidden mb-2 bg-gray-500">
        <h1 class="text-center py-14 text-2xl font-bold text-white">Upload</h1>
      </div>
      <v-btn
        :loading="loadingCoverPic"
        small
        color="orange lighten-1"
        class="white--text"
        @click="uploadCoverPic"
      >
        <div class="flex flex-row items-center">
          <v-icon small class="mr-2">mdi-cloud-upload</v-icon>
          <span>{{ coverpic ? "Change" : "Upload" }} Cover Pic</span>
        </div>
      </v-btn>
    </div>
    <!-- End of Upload Section -->
    <template>
      <v-card class="p-2 w-1/2">
        <v-container fluid>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                label="First Name"
                v-model="firstName"
                color="orange"
                required
                filled
                rows="2"
              ></v-text-field>
            </v-col>
            <v-col cols="12" sm="6">
              <v-text-field
                label="Last Name"
                v-model="lastName"
                color="orange"
                required
                filled
                rows="2"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea
                label="About Me"
                v-model="aboutMe"
                color="orange"
                filled
              >
              </v-textarea>
            </v-col>
            <v-card-actions>
              <v-btn class="mr-2" text @click="resetForm"> Cancel </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                right
                color="orange"
                class="white--text"
                @click="
                  onSubmitAboutMe(), onSubmitFirstName(), onSubmitLastName()
                "
                >Update</v-btn
              >
            </v-card-actions>
          </v-row>
        </v-container>
      </v-card>
    </template>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
import { nanoid } from "nanoid";
import { PutObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3";
export default {
  layout: "dashboard",
  layout: "dashboard",
  name: "account",
  data() {
    return {
      // The v-model bounded description
      aboutMe: null,
      firstName: null,
      lastName: null,
      loadingCoverPic: null,
      loadingProfilePic: null,
      profilepic: null,
      coverpic: null,
    };
  },
  computed: {
    ...mapGetters({
      user: "users/rootUser",
    }),
  },
  async mounted() {
    await this.$store.dispatch("users/userGet");
    this.loading = false;
  },

  methods: {
    uploadProfilePic() {
      document.getElementById("file-input").click();
    },
    uploadCoverPic() {
      document.getElementById("file-input2").click();
    },
    async profilePicSelected(event) {
      const file = event.target.files[0];
      const typeArr = file.type.split("/");
      this.loadingProfilePic = true;
      try {
        if (this.user[0].profilePicKey) {
          const urlArr = this.user[0].profilePicKey.split("/");
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
        this.profilepic = `https://videogenesis-profilepics.s3.us-west-2.amazonaws.com/${putPayload.Key}`;
      } catch (error) {
        console.error(error);
      }
      this.loadingProfilePic = false;
      this.onSubmitUserProfilePic();
    },
    async coverPicSelected(event) {
      const file = event.target.files[0];
      const typeArr = file.type.split("/");
      this.loadingCoverPic = true;
      try {
        if (this.user[0].coverPicKey) {
          const urlArr = this.user[0].coverPicKey.split("/");
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
        this.coverpic = `https://videogenesis-profilepics.s3.us-west-2.amazonaws.com/${putPayload.Key}`;
      } catch (error) {
        console.error(error);
      }
      this.loadingCoverPic = false;
      this.onSubmitUserCoverPic();
    },
    resetForm() {
      this.aboutMe = null;
      this.firstName = null;
      this.lastName = null;
    },
    async onSubmitAboutMe() {
      const aboutMe = await this.$store.dispatch("users/userPut", {
        usersAboutMe: this.aboutMe,
      });
    },
    async onSubmitUserProfilePic() {
      const userCoverPic = await this.$store.dispatch("users/userPut", {
        profilePicKey: this.userProfilePic,
      });
    },
    async onSubmitUserCoverPic() {
      const userCoverPic = await this.$store.dispatch("users/userPut", {
        coverPicKey: this.userCoverPic,
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
