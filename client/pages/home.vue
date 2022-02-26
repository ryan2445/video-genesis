<template>
  <div>
    <div class="my-52 relative">
      <div>
        <profile-banner />
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
            <div class="grid md:grid-cols-3 grid-cols-1 gap-x-2 items-center place-items-center">
              <video-card v-for="(video, i) in videos" :key="i" :video="video" :idx="i" />
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import ProfileBanner from "../components/ProfileBanner.vue";
export default {
  components: { ProfileBanner },
  layout: "dashboard",
  data() {
    return { tabSelected: "Uploads", loading: true };
  },
  computed: {
    ...mapGetters({
      user: "user/user",
      videos: "videos/videos",
    }),
  },
  methods: {
    changeTabSelection(tabName) {
      this.tabSelected = tabName;
    },
  },
  async mounted() {
    //  Send request to get videos

    await this.$store.dispatch("videos/videosGet");

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
