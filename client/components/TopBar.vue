<template>
  <v-app-bar
    app
    clipped-left
    elevation="1"
    style="z-index: 50 !important; background: #2e1226"
  >
    <div class="d-flex align-center">
      <NuxtLink to="/" class="mr-1">
        <!-- <img
          src="https://upload.wikimedia.org/wikipedia/commons/1/1a/V_logo.png"
          class="rounded-full object-cover"
          style="width: 45px; height: 45px"
        /> -->
        <svg
          width="35"
          height="35"
          viewBox="0 0 100 100"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          class="hover:fill-[#F8FFCA]"
        >
          <path
            d="M95.294 78.1272L95.32 78.1122L62.074 20.5302L62.06 20.5382C61.328 19.0362 59.8 17.9912 58.016 17.9912C57.1475 17.9922 56.2978 18.2442 55.5692 18.7168C54.8406 19.1895 54.264 19.8626 53.909 20.6552L31.784 58.9752L26.367 49.5932L26.36 49.5972C26.1666 49.1954 25.864 48.8562 25.4867 48.6185C25.1095 48.3808 24.6729 48.2542 24.227 48.2532C23.263 48.2532 22.436 48.8312 22.063 49.6552L6.271 77.0092H6.2V77.1312L4.671 79.7792C4.48681 80.0175 4.38661 80.31 4.386 80.6112C4.386 81.3752 5.005 81.9942 5.768 81.9942C5.92 81.9942 6.063 81.9642 6.2 81.9182V82.0092H93.2V81.9592C93.8557 81.9089 94.4683 81.6131 94.9156 81.131C95.3629 80.6489 95.6119 80.0159 95.613 79.3582C95.6107 78.9277 95.5011 78.5046 95.294 78.1272V78.1272Z"
            fill="#A13440"
          />
        </svg>
      </NuxtLink>
      <div class="text-white mt-1">
        <span class="font-bold">Video Genesis</span>
        {{ !!title ? " - " : "" }}{{ title }}
      </div>
    </div>
    <v-spacer />
    <div class="mx-6">
      <v-tooltip bottom>
        <template v-slot:activator="{ on, attrs }">
          <v-icon v-bind="attrs" v-on="on" color="grey lighten-2">
            {{ srRunning ? "icon-wifi-check" : "icon-wifi-cancel" }}
          </v-icon>
        </template>
        <span>
          Super Resolution server is {{ srRunning ? "" : "not" }} running!
        </span>
      </v-tooltip>
    </div>
    <v-menu offset-y min-width="200px">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          v-bind="attrs"
          v-on="on"
          fab
          depressed
          color="grey lighten-1"
          width="45"
          height="45"
        >
          <img
            v-if="userProfilePic"
            style="height: 45px; width: 45px"
            class="rounded-full object-cover"
            :src="userProfilePic"
          />
          <v-icon v-else> mdi-account </v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item-group color="orange">
          <v-list-item
            v-for="(item, i) in topBarItems"
            :key="i"
            @click="handleClick(item)"
          >
            <v-list-item-icon class="listItemIcon">
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-icon>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.title }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      topBarItems: [
        {
          title: "Account Settings",
          color: "orange",
          icon: "mdi-account",
          route: "/account",
        },
        {
          title: "Sign Out",
          icon: "mdi-logout-variant",
          method: "signOut",
        },
      ],
    };
  },
  methods: {
    handleClick(item) {
      if (item.route) return this.$router.push(item.route);

      if (item.method) return this[item.method]();
    },
    async signOut() {
      await this.$auth.signOut();
      this.$store.commit("users/rootUserSet", null);
      this.$store.commit("auth/clearToken");
      this.$router.push("/");
    },
  },
  computed: {
    title() {
      return this.$store.getters["app/route"];
    },
    ...mapGetters({
      user: "users/rootUser",
      srRunning: "sr/running",
    }),
    userProfilePic() {
      // If the user does not exist, return null
      if (!this.user) return null;

      return this.user.profilePicKey;
    },
  },
};
</script>
<style scoped>
.v-application--is-ltr .v-list-item__action:first-child,
.v-application--is-ltr .v-list-item__icon:first-child {
  margin-right: 16px;
}
</style>
