<template>
  <v-navigation-drawer v-model="drawer" :mini-variant.sync="mini" app>
    <v-list-item  class="px-2 my-1" color="orange">
      <v-list-item-avatar>
        <img alt="Avatar" :src="userImage" />
      </v-list-item-avatar>

      <div class="text-h6">{{ userName }}</div>
    </v-list-item>

    <v-divider></v-divider>

    <v-list nav>
      <v-list-item-group color="orange lighten-1">
        <v-list-item
          v-for="[icon, text, link] in links"
          :key="icon"
          :to="link"
          link
        >
          <v-list-item-icon>
            <v-icon>{{ icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
    <template v-slot:append>
      <v-divider></v-divider>
      <v-btn
       icon
       @click.stop="mini = !mini"
       >
      <v-icon class="mx-10 my-2">mdi-menu</v-icon>
      </v-btn>
    </template>
  </v-navigation-drawer>
</template>

<script>
export default {
  data: () => ({
    userName: "Dalidrew",
    userImage:
      "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1760&q=80",
    drawer: true,
    links: [
      ["mdi-home", "Home", "/home"],
      ["mdi-upload", "Upload", "/upload"],
      ["mdi-view-list", "Videos", "/videos"],
    ],
    mini: false, 
  }),
};
</script>

<style scoped></style>
