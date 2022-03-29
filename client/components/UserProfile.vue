<template>
  <div class="flex flex-1 relative flex-col">
    <div v-if="!loading">
      <profile-banner :user="user" />
      <div style="border: 1px solid black">
        <div>
          <v-tabs
            v-model="tabSelected"
            centered
            background-color="#0000"
            color="orange"
          >
            <v-tab
              v-for="(tab) in tabs"
              :key="tab"
            >
              {{ tab }}
            </v-tab>
          </v-tabs>
        </div>
      </div>
    </div>
    <div class="flex flex-1">
      <transition mode="out-in">
        <div
          v-if="tabSelected == 0"
          class="mt-10 ml-auto mr-auto"
        >
          <video-list :videos="videos" />
        </div>
        <div
          v-else-if="tabSelected == 1"
          class="mt-10 ml-auto mr-auto w-3/4"
        >
          <profile-about :user="user" />
        </div>
        <div
          v-else-if="tabSelected == 2"
          class="mt-10 ml-auto mr-auto"
        >
          <div class="flex flex-row flex-wrap justify-start">
            <profile-playlists :user="user" />
          </div>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: "UserProfile",
  props: {
    user: {
      type: Object,
      required: true
    },
  },
  data() {
    return {
      tabs: ['Uploads', 'About', 'Playlists'],
      tabSelected: 'Uploads',
      loading: true,
    };
  },
  methods: {
    changeTabSelection(tabName) {
      this.tabSelected = tabName;
    },
  },
  async mounted() {
    const videos = await this.$store.dispatch("videos/videosGetByUsername", {
      username: this.user.username,
    });
    
    this.$store.commit("videos/videosSet", videos);

    this.loading = false;
  },
  computed: {
    ...mapGetters({
        videos: "videos/videos",
    }),
  }
};
</script>
