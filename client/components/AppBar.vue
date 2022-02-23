<template>
  <v-row justify="space-between" align="center" no-gutters>
    <v-col cols="2">
      <h1 class="font-medium text-xl mx-4">Video Genesis</h1>
    </v-col>
    <v-col cols="10">
      <v-row align="center" justify="end" no-gutters>
        <v-btn
          color="#FF7A45"
          outlined
          class="m-2"
          v-if="!user"
          @click="onSignUp"
        >
          Sign Up
        </v-btn>
        <v-btn
          class="white--text"
          color="orange accent-3"
          v-if="!user"
          @click="onSignIn"
        >
          Sign In
        </v-btn>
        <div class="mx-3" v-if="!!user">
          <h1>Logged in as {{ user.username }}</h1>
        </div>
        <v-btn v-if="!!user" @click="onSignOut"> Sign Out </v-btn>
      </v-row>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "AppBar",
  methods: {
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

        this.$store.commit("user/setUser", null);
        this.$store.dispatch("auth/unauthorize", { axios: this.$axios });

        console.log("EVENT: User signed out");
      } catch (error) {
        console.log("error signing out: ", error);
      }
    },
  },
  computed: {
    ...mapGetters({
      user: "user/user",
    }),
  },
};
</script>
