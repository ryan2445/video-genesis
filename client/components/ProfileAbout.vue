<template>
  <div class="w-3/4">
    <h1 class="text-xl font-bold mb-1 ml-2">About</h1>
    <hr class="border-t-1 border-solid border-black mb-3" />
    <p class="text-base">{{ this.user[0].usersAboutMe }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      aboutme: null,
    };
  },

  computed: {},
  props: {
    user: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style></style>
