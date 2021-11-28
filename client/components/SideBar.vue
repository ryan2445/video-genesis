<template>
  <v-navigation-drawer v-model="drawer" width="256px" app>
    <v-sheet color="orange lighten-3" class="pa-4">
      <v-avatar class="mb-4" color="grey lighten-1" size="64">
        <img alt="Avatar" :src="userImage" />
      </v-avatar>

      <div class="text-h6">{{ userName }}</div>
    </v-sheet>

    <v-divider></v-divider>

    <v-list 
    nav>
      <v-list-item-group
      color="orange lighten-1"
      
      >
        <v-list-item v-for="[icon, text, link] in links" :key="icon" :to="link" link>
          <v-list-item-icon>
            <v-icon>{{ icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ text }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list-item-group>
    </v-list>
   <div> 
   <v-divider></v-divider>
   <v-icon class="mx-2 my-2">mdi-menu</v-icon> 
   </div>
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
  }),
};
</script>

<style scoped>
</style>