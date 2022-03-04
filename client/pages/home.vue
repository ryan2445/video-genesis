<template>
  <user-profile v-if="user" :user="user" :root="true" />
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
      user: "users/rootUser",
      videos: "videos/videos",
    }),
  },
  methods: {
    changeTabSelection(tabName) {
      this.tabSelected = tabName;
    },
  },
  async mounted() {
    await this.$store.dispatch("users/userGet")

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
