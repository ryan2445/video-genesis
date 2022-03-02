<template>
  <div>
    <div class="my-52 relative">
      <div v-if="!loading">
        <profile-banner :user="user2" />
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
        <transition mode="out-in">
          <div
            v-if="tabSelected == 'Uploads' && loading == false"
            class="mt-10 ml-auto mr-auto"
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
            <profile-about :user="user2" />
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import ProfileAbout from "../components/ProfileAbout.vue";
import ProfileBanner from "../components/ProfileBanner.vue";
export default {
  components: { ProfileBanner, ProfileAbout },
  layout: "dashboard",
  data() {
    return {
      tabSelected: "Uploads",
      loading: true,
      profilepic: null,
      coverpic: null,
      usernull: null,
    };
  },
  computed: {
    ...mapGetters({
      user: "user/user",
      user2: "users/rootUser",
      videos: "videos/videos",
    }),
  },
  methods: {
    changeTabSelection(tabName) {
      this.tabSelected = tabName;
    },
  },
  created() {
    this.$store.commit("app/setRoute", this.user.username);
  },
  async mounted() {
    //  Send request to get videos
    await this.$store.dispatch("videos/videosGet");
    await this.$store.dispatch("users/userGet");

    //  Stop loading
    this.loading = false;
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
