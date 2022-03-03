<template>
  <div>
    <div class="my-52 relative">
      <div>
        <profile-banner v-if="user" :user="user" />
      </div>
      <div class="absolute mt-0 w-full">
        <div class="flex mx-72 space-x-10 mt-5">
          <div
            class="text-xl hover:text-yellow-500 cursor-pointer"
            :class="{
              'border-b-4 border-yellow-500  border-solid text-yellow-500':
                tabSelected == 'Uploads',
            }"
          >
            <h1 @click="changeTabSelection('Uploads')">UPLOADS</h1>
          </div>

          <div
            class="text-xl hover:text-yellow-500 cursor-pointer"
            :class="{
              'border-b-4 border-yellow-500  border-solid text-yellow-500':
                tabSelected == 'About',
            }"
          >
            <h1 @click="changeTabSelection('About')">ABOUT</h1>
          </div>
        </div>
        <transition>
          <div
            v-if="tabSelected == 'Uploads' && loading == false"
            class="mt-10 ml-auto mr-auto w-3/4"
          >
            <div
              class="grid md:grid-cols-3 grid-cols-1 gap-x-2 items-center place-items-center"
            >
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
            <profile-about v-if="user" :user="user" />
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import ProfileBanner from "../../components/ProfileBanner.vue";
export default {
  components: { ProfileBanner },
  layout: "dashboard",
  data() {
    return { tabSelected: "Uploads", loading: true, username: "",  user: undefined, videos: [] };
  },
  methods: {
    changeTabSelection(tabName) {
      this.tabSelected = tabName;
    },
    getQueryParamsAndSetKeys() {
      const path = this.$route.fullPath.replace('/users/', '');
      const params = new URLSearchParams(path);

      // If the username is not provided, error
      if (!params.has('username')) {
        return;
      }

      const username = params.get('username');
      this.username = username; 
     
    },
  },
  created() {
    this.$store.commit("app/setRoute", "");
  },
  async mounted() {
    //  Send request to get videos
    await this.$store.dispatch("videos/videosGet");

    //  Stop loading
    this.loading = false;
    this.getQueryParamsAndSetKeys()
    const user = await this.$store.dispatch("users/userGetByUsername", {username: this.username}); 
    this.user = user;
    const videos = await this.$store.dispatch("videos/videosGetByUsername", {username: this.username}); 
    this.videos = videos;
  },
};
</script>

<style scoped>
.v-enter-active,
.v-leave-active {
  transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
  opacity: 0;
}
</style>
