<template>
  <div class="page-container h-screen">
    <v-row>
      <v-col cols="7" class="px-16 mt-16 text-white">
        <h2
          @click="handleOnClick"
          class="text-4xl font-bold"
          :class="{ 'cursor-pointer hover:text-yellow-100': !!user }"
        >
          Video Genesis
        </h2>
        <h5 class="text-2xl">Super-Resolution Video For Everyone</h5>
        <p class="mt-4 w-3/4">
          Video Genesis is a video streaming platform that enables users to
          upscale their videos from low to high-resolution using a
          Super-Resolution Generative Adversarial Network (SRGAN). SGRAN is a
          trained machine learning model that predicts high-resolution images
          from their low-resolution counterparts. Videos that are processed
          using this model can be displayed side-by-side with their original and
          down-sampled versions for comparison. Users can stream videos and
          interact with other content creators by leaving comments on videos.
          Videos can be organized in playlists and played sequentially. Unlike
          other platforms, Video Genesis opens up the pathway to intuitively
          interact with super-resolution technology.
        </p>
        <p class="opacity-50">
          CS 426 Senior Project in Computer Science, Spring 2022, at UNR, CSE
          Department
        </p>
      </v-col>
      <v-col cols="5" class="px-16 mt-16">
        <div v-if="!user" class="float-right">
          <v-btn text class="m-2 white--text" @click="onSignIn">
            Sign In
          </v-btn>
          <v-btn class="white--text" color="#A13440" @click="onSignUp">
            Sign Up
          </v-btn>
        </div>
        <div
          v-else
          class="flex flex-row items-center"
          style="justify-content: end"
        >
          <div class="mx-3" v-if="user">
            <h1>Logged in as {{ user.username }}</h1>
          </div>
          <v-btn v-if="user" @click="onSignOut"> Sign Out </v-btn>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "AppBar",
  methods: {
    handleOnClick() {
      if (!this.user) return;

      this.$router.push("/home");
    },
    onSignUp() {
      this.$router.push({
        path: "/auth/sign-up",
      });
    },
    onSignIn() {
      this.$router.push({
        path: "/auth/sign-in",
      });
    },
    async onSignOut() {
      try {
        await this.$auth.signOut();

        this.$store.commit("users/rootUserSet", null);
        this.$store.commit("auth/clearToken");
        this.$router.push("/");
      } catch (error) {
        console.log("error signing out: ", error);
      }
    },
  },
  computed: {
    ...mapGetters({
      user: "users/rootUser",
    }),
  },
};
</script>

<style scoped></style>
