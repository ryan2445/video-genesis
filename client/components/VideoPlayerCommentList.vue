<template>
  <div>
    <div v-if="!loadingInitial">
      <video-player-comment-box
        v-for="(comment, index) in comments"
        :key="index"
        :comment="comment"
        :user="users[index]"
      />
    </div>
  </div>
</template>

<script>
import VideoPlayerCommentBox from "./VideoPlayerCommentBox.vue";
export default {
  components: { VideoPlayerCommentBox },
  props: {
    video: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    loadingInitial: true,
    comments: null,
    users: null,
  }),
  async mounted() {
    try {
      this.comments = await this.getCommentsForVideo();
      this.users = await this.getUsersForComments();
      this.loadingInitial = false;
    } catch (e) {
      return null;
    }
  },
  methods: {
    async getCommentsForVideo() {
      try {
        const response = await this.$axios.get(
          `comments?videoId=${this.video.sk.split("#")[1]}`
        );
        return response.data;
      } catch (exception) {
        return null;
      }
    },
    async getUsersForComments() {
      let promises = [];
      for (let i = 0; i < this.comments.length; i += 1) {
        promises.push(
          this.$axios.get(`users/all?username=${this.comments[i].userId}`)
        );
      }
      let results = await Promise.all(promises);
      let data = results.map((element) => {
        return element.data;
      });

      return data;
    },
  },
};
</script>

<style></style>
