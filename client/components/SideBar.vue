<template>
  <v-navigation-drawer app clipped :mini-variant="drawer">
    <v-divider></v-divider>
    <v-list nav>
      <v-list-item-group color="#A13440">
        <v-list-item v-for="(item, i) in items" :key="i" :to="item.route" link>
          <v-tooltip right :open-delay="250">
            <template v-slot:activator="{ on, attrs }">
              <v-list-item-icon v-bind="attrs" v-on="on">
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
            </template>
            <span>{{ item.title }}</span>
          </v-tooltip>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <template v-slot:append>
      <v-btn class="mx-2" icon @click.stop="drawer = !drawer">
        <v-icon class="mx-10 my-2">mdi-menu</v-icon>
      </v-btn>
    </template>
  </v-navigation-drawer>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  data: () => ({
    items: [
      {
        title: "Home",
        icon: "mdi-home",
        route: "/home",
      },
      {
        title: "Upload",
        icon: "mdi-upload",
        route: "/upload",
      },

      {
        title: "Explore",
        icon: "mdi-telescope",
        route: "/explore",
      },
      {
        title: "Contact Us",
        icon: "mdi-account-question ",
        route: "/contactus",
      },
    ],
    drawer: true,
  }),
  computed: {
    ...mapGetters({
      user: "users/rootUser",
    }),
  },
};
</script>
