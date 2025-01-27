<template>
  <div class="flex flex-1 relative flex-col">
    <div class="mb-4 rounded-br-lg rounded-bl-lg" style="background: #fff">
      <profile-banner :user="user" />
      <div class="w-full flex justify-center items-center">
        <div class="w-1/2">
          <v-tabs
            v-model="tabSelected"
            centered
            background-color="#0000"
            color="#A13440"
          >
            <v-tab v-for="tab in tabs" :key="tab">
              {{ tab }}
            </v-tab>
          </v-tabs>
        </div>
        <upload-video-button v-if="permissions" />
      </div>
    </div>
    <div style="background: #fff" class="rounded-lg px-3 py-2 relative">
      <v-carousel
        v-if="!loading"
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
    async init() {
      this.loading = true;

      const videos = await this.$store.dispatch("videos/videosGetByUsername", {
        username: this.user.username,
      });

      this.$store.commit("videos/videosSet", videos);

      const playlists = await this.$store.dispatch(
        "playlists/playlistsGetByUsername",
        {
          username: this.user.username,
        }
      );

      this.$store.commit("playlists/playlistsSet", playlists);

      this.loading = false;
    },
  },
  async mounted() {
    this.init();
  },
  computed: {
    ...mapGetters({
      videos: "videos/videos",
      playlists: "playlists/playlists",
    }),
    tabComponents() {
      return [
        {
          name: "video-list",
          props: {
            videos: this.videos,
            playlists: this.playlists,
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
    permissions() {
      const rootUser = this.$store.getters["users/rootUser"];

      if (!rootUser) return false;

      return rootUser.pk === this.user.pk && rootUser.sk === this.user.sk;
    },
  },
  watch: {
    user() {
      this.init();
    },
  },
};
</script>
