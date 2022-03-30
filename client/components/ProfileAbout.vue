<template>
  <div class="w-3/4">
    <p class="text-base">
      {{ this.user.usersAboutMe }}
      </p>
  </div>
</template>

<script>
export default {
  name: "ProfileAbout",
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style></style>
