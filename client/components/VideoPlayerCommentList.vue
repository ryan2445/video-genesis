<template>
  <div></div>
</template>

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
    this.comments = await this.getCommentsForVideo();
    console.log("hello");
  },
  methods: {
    async getCommentsForVideo() {
      try {
        console.log(this.video.sk);
        const response = await this.$axios.get(
          `comments?videoId=${this.video.sk.split("#")[1]}`
        );
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
