<template>
  <div>
    <div v-if="loading" class="text-center" style="height: 100vh">
      <v-progress-circular indeterminate color="orange" style="top: 50%" />
    </div>

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
        <h1 class="text-center py-12 text-xl font-bold text-white">Upload</h1>
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
          <span>{{ userProfilePic ? "Change" : "Upload" }} Profile Pic</span>
        </div>
      </v-btn>
    </div>
    <!-- User Cover Pic -->
    <div class="mb-4">
      <div v-if="userCoverPic" class="h-36 w-1/2 overflow-hidden mb-2">
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
        :loading="loading"
        small
        color="orange lighten-1"
        class="white--text"
        @click="uploadCoverPic"
      >
        <div class="flex flex-row items-center">
          <v-icon small class="mr-2">mdi-cloud-upload</v-icon>
          <span>{{ userCoverPic ? "Change" : "Upload" }} Cover Pic</span>
        </div>
      </v-btn>
    </div>

    <!-- End of Upload Section -->
    <template>
      <v-card>
        <v-container fluid>
          <v-row>
            <v-col cols="12" sm="6">
              <v-text-field
                label="First Name"
                v-model="firstName"
                color="orange"
                @change="onChange"
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
                @change="onChange"
                required
                filled
                rows="2"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-textarea v-model="aboutMe" color="orange" @change="onChange">
                <template v-slot:label>
                  <div>About Me</div>
                </template>
              </v-textarea>
            </v-col>
            <v-card-actions>
              <v-btn text @click="resetForm"> Cancel </v-btn>
              <v-spacer></v-spacer>
              <v-btn
                right
                color="orange"
                @click="
                  onSubmitAboutMe(false),
                    onSubmitFirstName(false),
                    onSubmitLastName(false)
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
