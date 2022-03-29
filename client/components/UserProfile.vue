<template>
  <div class="w-full flex justify-center">
    <div class="relative" style="min-width: 1280px">
      <div v-if="!loading">
        <profile-banner :user="user" />
        <div style="border: 1px solid black">
          <div class="flex flex-row py-3">
            <div
              class="text-xl hover:text-yellow-500 cursor-pointer ml-64"
              :class="{
                'border-b-4 border-yellow-500  border-solid text-yellow-500':
                  tabSelected == 'Uploads',
              }"
            >
              <h1 @click="changeTabSelection('Uploads')">UPLOADS</h1>
            </div>

            <div
              class="text-xl hover:text-yellow-500 cursor-pointer mx-4"
              :class="{
                'border-b-4 border-yellow-500  border-solid text-yellow-500':
                  tabSelected == 'About',
              }"
            >
              <h1 @click="changeTabSelection('About')">ABOUT</h1>
            </div>
            <div
              class="text-xl hover:text-yellow-500 cursor-pointer mx-4"
              :class="{
                'border-b-4 border-yellow-500  border-solid text-yellow-500':
                  tabSelected == 'Playlists',
              }"
            >
              <h1 @click="changeTabSelection('Playlists')">PLAYLISTS</h1>
            </div>
          </div>
        </div>
      </div>
      <div class="absolute mt-0 w-full">
        <transition mode="out-in">
          <div
            v-if="tabSelected == 'Uploads' && loading == false"
            class="mt-10 ml-auto mr-auto"
          >
            <div class="flex flex-row flex-wrap justify-start">
              <video-card
                v-for="(video, i) in videos"
                :key="i"
                :video="video"
                :idx="i"
              />
            </div>
          </div>
          <div
            v-else-if="tabSelected == 'About' && !loading"
            class="mt-10 ml-auto mr-auto w-3/4"
          >
            <profile-about :user="user" />
          </div>
          <div
            v-if="tabSelected == 'Playlists' && loading == false"
            class="mt-10 ml-auto mr-auto"
          >
            <div class="flex flex-row flex-wrap justify-start">
              <profile-playlists :user="user" />
            </div>
          </div>
        </transition>
      </div>
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
      tabSelected: "Uploads",
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

    //  Stop loading
    this.loading = false;
  },
  computed: {
    ...mapGetters({
      videos: "videos/videos",
    }),
  },
};
</script>
