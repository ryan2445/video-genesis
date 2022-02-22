<template>
  <v-navigation-drawer v-model="drawer" :mini-variant.sync="mini" app>
    <template v-slot:prepend>
      <v-list-item class="px-2 orange lighten-1">
        <v-list-item-avatar>
          <img alt="Avatar" :src="userImage" />
        </v-list-item-avatar>
        <div class="text-white font-weight-bold">Video Genesis</div>
      </v-list-item>
    </template>
    <v-divider></v-divider>
    <v-list nav>
      <v-list-item-group color="orange lighten-1">
        <v-list-item v-for="(item, i) in items" :key="i" :to="item.route" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <template v-slot:append>
      <v-divider></v-divider>
      <v-btn class="mx-2" icon @click.stop="mini = !mini">
        <v-icon class="mx-10 my-2">mdi-menu</v-icon>
      </v-btn>
    </template>
  </v-navigation-drawer>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  data: () => ({
    drawer: true,
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
        title: "Videos",
        icon: "mdi-view-list",
        route: "/videos",
      },
      {
        title: "Explore",
        icon: "mdi-view-list",
        route: "/explore",
      },
    ],
    mini: false,
    userImage: "https://upload.wikimedia.org/wikipedia/commons/1/1a/V_logo.png",
  }),
  computed: {
    ...mapGetters({
      user: "user/user",
    }),
  },
};
</script>
<style scoped></style>
