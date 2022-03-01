<template>
  <div>
    <div class="my-52 relative">
      <div>
        <profile-banner />
      </div>
      <div class="absolute mt-0 w-full"></div>
    </div>

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
