<template>
  <div class="mt-4">
    <video-player-comment-form :video="video" class="mb-4" />
    <div v-if="loadingInitial && allcomments != null">
      <v-progress-circular indeterminate color="amber"></v-progress-circular>
    </div>
    <div v-if="!loadingInitial" ref="listComponent">
      <video-player-comment-box
        v-for="(comment, index) in allcomments"
        :key="index"
        :comment="comment"
        :user="users[index]"
      />
      <infinite-loading @infinite="loadMoreComments">
        <div slot="spinner">
          <v-progress-circular
            indeterminate
            color="amber"
          ></v-progress-circular>
        </div>
        <div slot="no-more" class="-mb-2">
          <p class="text-gray-500">No More Comments</p>
        </div>
      </infinite-loading>
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
        // const response = await this.$axios.get(
        //   `comments?videoId=${this.video.sk.split("#")[1]}`
        // );
        const response = await this.$axios.get("comments", {
          params: {
            videoId: this.video.sk.split("#")[1],
            lastKey: "initialQuery",
          },
        });
        console.log(response);
        this.arrOfPageKey.push(response.data.LastEvaluatedKey.sk.split("#")[1]);
        this.currentcomments = response.data.Items;
        return response.data.Items;
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
      try {
        const response = await this.$axios.get("comments", {
          params: {
            videoId: this.video.sk.split("#")[1],
            lastKey: this.arrOfPageKey.pop(),
          },
        });
        this.currentcomments = response.data.Items;
        let currentusers = await this.getUsersForComments();
        $state.loaded();
        if (response.data.LastEvaluatedKey == undefined) {
          $state.complete();
        }
        this.allcomments.push(...this.currentcomments);
        this.users.push(...currentusers);
        console.log(response.data.LastEvaluatedKey.sk.split("#")[1]);
        this.arrOfPageKey.push(response.data.LastEvaluatedKey.sk.split("#")[1]);
        return response.data;
      } catch (exception) {
        return null;
      }
    },
  },
};
</script>

<style></style>
