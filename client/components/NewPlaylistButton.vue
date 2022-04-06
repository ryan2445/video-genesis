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
        class="-top-8 -right-1"
        v-bind="attrs"
        v-on="on"
      >
        <span class="text-app-orange">
          {{ text }}
        </span>
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