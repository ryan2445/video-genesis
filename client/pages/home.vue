<template>
  <div class="my-36">
    <profile-banner />
    <v-content>
      <h1 class="mt-10 text-xl">Hello</h1>
    </v-content>
  </div>
</template>

<script>
import ProfileBanner from "../components/ProfileBanner.vue";
export default {
  components: { ProfileBanner },

  layout: "dashboard",
};
</script>

<style scoped></style>
