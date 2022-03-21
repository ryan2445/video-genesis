<template>
  <v-app-bar app color="orange" :elevation="1" hide-on-scroll style="height:56px;">
    <div>
      <h2 class="text-gray-800 text-lg strong">
        {{ title }}
      </h2>
    </div>
    <v-spacer />
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
          class="mb-2 shadow-md"
        >
      <!-- <v-icon> mdi-account </v-icon> -->
        <div
            v-if="userProfilePic"
            class="w-14 h-14 rounded-full overflow-hidden mb-2"
        >
          <img
              class="min-w-full min-h-full object-cover"
              :src="userProfilePic"
              alt="avatar"
          />
        </div>
          
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
      this.$store.commit("user/setUser", null);
      this.$store.dispatch("auth/unauthorize", { axios: this.$axios });
      this.$router.push("/");
    },
  },
  computed: {
    title() {
      return this.$store.getters["app/route"];
    },
    ...mapGetters({
      user: "users/rootUser",
    }),
    userProfilePic() {
      // If the user does not exist, return null
      if (!this.user) return null;

      return this.user.profilePicKey || "https://www.unr.edu/main/images/divisions/president/marketing-communications/brand/brand-athletics-2.png";
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
