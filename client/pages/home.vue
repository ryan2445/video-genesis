<template>
  <user-profile v-if="user" :user="user" :root="true" />
</template>

<script>
import { mapGetters } from "vuex";
export default {
  layout: "dashboard",
  data() {
    return {
      tabSelected: "Uploads",
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
    if (!this.user) await this.$store.dispatch("users/userGet");

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
