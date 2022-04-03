<template></template>

<script>
export default {
  props: {
    video: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    loading: true,
    comments: null,
  }),
  async mounted() {
    await this.getCommentsForVideo();
    console.log("hello");
  },
  methods: {
    async getCommentsForVideo() {
      try {
        console.log(this.video.sk);
        const response = await this.$axios.get(
          `comments?videoId=${this.video.sk.split("#")[1]}`
        );
        console.log(response.data);
        return response.data;
      } catch (exception) {
        return null;
      }
      this.loading = false;
    },
  },
};
</script>

<style></style>
