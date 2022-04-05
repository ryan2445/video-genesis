<template>
  <div class="mt-10">
    <div v-if="!loadingInitial" ref="listComponent">
      <video-player-comment-box
        v-for="(comment, index) in allcomments"
        :key="index"
        :comment="comment"
        :user="users[index]"
      />
      <infinite-loading @infinite="loadMoreComments"></infinite-loading>
    </div>
  </div>
</template>

<script>
import VideoPlayerCommentBox from "./VideoPlayerCommentBox.vue";
import InfiniteLoading from "vue-infinite-loading";
export default {
  components: { VideoPlayerCommentBox, InfiniteLoading },
  props: {
    video: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    loadingInitial: true,
    currentcomments: null,
    allcomments: null,
    arrOfPageKey: [],
    users: null,
  }),
  async mounted() {
    try {
      this.allcomments = await this.getCommentsForVideo();
      this.users = await this.getUsersForComments();
      this.loadingInitial = false;
      window.addEventListener("scroll", handleScroll);
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
        this.currentcomments = response.data;
        let pk = response.data[9].pk;
        let sk = response.data[9].sk;
        let LastKey = { pk, sk };
        console.log(LastKey);
        console.log(response);
        return response.data;
      } catch (exception) {
        return null;
      }
    },
    async getUsersForComments() {
      let promises = [];
      for (let i = 0; i < this.currentcomments.length; i += 1) {
        promises.push(
          this.$axios.get(
            `users/all?username=${this.currentcomments[i].userId}`
          )
        );
      }
      let results = await Promise.all(promises);
      let data = results.map((element) => {
        return element.data;
      });

      return data;
    },
    async loadMoreComments($state) {
      this.currentcomments = await this.getCommentsForVideo();
      let currentusers = await this.getUsersForComments();
      $state.loaded();
      console.log(this.currentcomments);
      this.allcomments.push(...this.currentcomments);
      this.users.push(...currentusers);
    },
  },
};
</script>

<style></style>
