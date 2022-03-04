<template>
  <div class="w-3/4">
    <h1 class="text-xl font-bold mb-1 ml-2">
      About
    </h1>
    <hr class="border-t-1 border-solid border-black mb-3" />
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
