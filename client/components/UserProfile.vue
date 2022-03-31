<template>
  <div class="flex flex-1 relative flex-col">
    <div class="mb-4 rounded-br-lg rounded-bl-lg" style="background: #fff">
      <profile-banner :user="user" />
      <div>
        <div>
          <v-tabs
            v-model="tabSelected"
            centered
            background-color="#0000"
            color="orange"
          >
            <v-tab v-for="tab in tabs" :key="tab">
              {{ tab }}
            </v-tab>
          </v-tabs>
        </div>
      </div>
    </div>
    <div style="background: #fff" class="rounded-lg px-3 py-2">
      <v-carousel
        v-model="tabSelected"
        hide-delimiter-background
        hide-delimiters
        touchless
        :show-arrows="false"
        class="userProfileCarousel"
        active-class="user-carousel-item"
        height="100%"
      >
        <v-carousel-item
          v-for="(comp, i) of tabComponents"
          :key="`carousel-${i}`"
          active-class="user-carousel-item"
        >
          <div>
            <h2 class="text-lg font-bold">
              {{ tabs[tabSelected] }}
            </h2>
            <v-divider></v-divider>
          </div>
          <component v-bind:is="comp.name" v-bind="comp.props"></component>
        </v-carousel-item>
      </v-carousel>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "UserProfile",
  props: {
    user: {
      type: Object,
      required: true,
    },
    playlist: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      tabs: ["Uploads", "About", "Playlists"],
      tabSelected: 0,
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
    tabComponents() {
      return [
        {
          name: "video-list",
          props: {
            videos: this.videos,
          },
          title: true,
        },
        {
          name: "profile-about",
          props: {
            user: this.user,
          },
        },
        {
          name: "profile-playlists",
          props: {
            user: this.user,
          },
        },
      ];
    },
  },
};
</script>
