<template>
  <user-profile v-if="user" :user="user" />
</template>

<script>
export default {
  name: "UserProfilePage",
  layout: "dashboard",
  data() {
    return { 
      tabSelected: "Uploads", 
      loading: true, 
      username: "", 
      user: undefined,
      videos: [] 
    };
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
    this.getQueryParamsAndSetKeys()
    const user = await this.$store.dispatch("users/userGetByUsername", this.username);
    
    this.user = user;

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
