<template>
  <v-menu 
    v-model="showPlaylistForm" 
    offset-y nudge-left="435" 
    nudge-bottom="2" 
    :close-on-content-click="false"
  >
    <template v-slot:activator="{ on, attrs }">
      <v-btn
        absolute
        small
        class="-top-8 -right-1"
        v-bind="attrs"
        v-on="on"
      >
        <div class="text-app-orange">
          <v-icon small class="mr-2">
            mdi-folder-plus
          </v-icon>
          {{ text }}
        </div>
      </v-btn>
    </template>
    <playlist-form @close="showPlaylistForm = false"></playlist-form>
  </v-menu>
</template>

<script>
export default {
  name: "NewPlayListButton",
  props: {
    text: {
      required: false,
      default: "New Playlist",
      type: String
    }
  },
  data() {
    return {
      showPlaylistForm: false
    }
  }
}
</script>
