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
  },
  methods: {
    async getCommentsForVideo() {
      try {
        console.log(this.video.sk);
        const response = await this.$axios.get(
          `comments?videoId=${this.video.sk.split("#")[1]}`
        );
        this.loading = false;
        return response.data;
      } catch (exception) {
        return null;
      }
    },
  },
};
</script>

<style></style>
