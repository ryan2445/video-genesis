<template>
  <v-app-bar app flat color="white">
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
        >
          <v-icon> mdi-account </v-icon>
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
import { mapGetters } from "vuex"
export default {
  data() {
    return {
      topBarItems: [
        {
          title: "Account Settings",
          icon: "mdi-account",
          route: "/account"
        },
        {
          title: "Sign Out",
          icon: "mdi-logout-variant",
          method: "signOut"
        }
      ]
    }
  },
  computed: {
    ...mapGetters({
      user: "user/user"
    })
  },
  methods: {
    handleClick(item) {
      if (item.route) return this.$router.push(item.route)

      if (item.method) return this[item.method]()
    },
    async signOut() {
      await this.$auth.signOut()
      this.$store.commit("user/setUser", null)
      this.$store.dispatch("auth/unauthorize", { axios: this.$axios })
      this.$router.push("/")
    }
  }
}
</script>
<style scoped>
.v-application--is-ltr .v-list-item__action:first-child,
.v-application--is-ltr .v-list-item__icon:first-child {
  margin-right: 16px;
}
</style>
