<template>
  <div class="mt-4">
    <video-player-comment-form
      :video="video"
      class="mb-4"
      v-on:addCommentToTheTop="addCommentToTheTop()"
    />
    <div v-if="loadingInitial && allcomments != null">
      <v-progress-circular indeterminate color="amber"></v-progress-circular>
    </div>
    <div v-if="!loadingInitial" ref="listComponent">
      <video-player-comment-box
        v-for="(comment, index) in allcomments"
        :key="index"
        :comment="comment"
        :index="index"
        :user="users[index]"
        v-on:deleteCommentFromTheTop="deleteCommentFromTheTop"
      />

      <infinite-loading @infinite="loadMoreComments">
        <div slot="spinner">
          <v-progress-circular
            indeterminate
            color="amber"
          ></v-progress-circular>
        </div>
        <div slot="no-more" class="-mb-2">
          <p class="text-gray-500">End of Comments</p>
        </div>

        <div slot="no-results" v-if="allcomments.length == 0" class="-mb-2">
          <p class="text-gray-500">Add a comment</p>
        </div>
        <div slot="no-results" v-else class="-mb - 2">
          <p class="text-gray-500">End of Comments</p>
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
    lastKey: "initialQuery",
  }),
  async mounted() {
    try {
      await this.getCommentsForVideo();
      this.users = await this.getUsersForComments();
      this.loadingInitial = false;
    } catch (e) {
      return null;
    }
  },

  methods: {
    async getCommentsForVideo($state) {
      try {
        // const response = await this.$axios.get(
        //   `comments?videoId=${this.video.sk.split("#")[1]}`
        // );

        const response = await this.$axios.get("comments/all", {
          params: {
            videoId: this.video.sk.split("#")[1],
            lastKey: this.lastKey,
          },
        });

        console.log(response);
        if (response.data.LastEvaluatedKey) {
          this.arrOfPageKey.push(
            response.data.LastEvaluatedKey.sk.split("#")[1]
          );
        }

        this.currentcomments = response.data.Items;

        this.allcomments = this.currentcomments;
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
        if (this.allcomments.length >= 10) {
          const response = await this.$axios.get("comments/all", {
            params: {
              videoId: this.video.sk.split("#")[1],
              lastKey: this.arrOfPageKey.pop(),
            },
          });
          $state.loaded();
          this.currentcomments = response.data.Items;
          let currentusers = await this.getUsersForComments();
          this.allcomments.push(...this.currentcomments);
          this.users.push(...currentusers);
          if (response.data.LastEvaluatedKey) {
            console.log(response.data.LastEvaluatedKey.sk.split("#")[1]);
            this.arrOfPageKey.push(
              response.data.LastEvaluatedKey.sk.split("#")[1]
            );
          }

          console.log(this.arrOfPageKey);
          if (!this.arrOfPageKey.length) {
            $state.complete();
          }

          return response.data;
        } else {
          $state.complete();
        }
      } catch (exception) {
        return null;
      }
    },

    async addCommentToTheTop() {
      try {
        const response = await this.$axios.get("comments", {
          params: {
            videoId: this.video.sk.split("#")[1],
          },
        });
        this.currentcomments = response.data.Items;
        let currentusers = await this.getUsersForComments();
        this.allcomments.unshift(...this.currentcomments);
        this.users.unshift(...currentusers);
      } catch (exception) {
        return null;
      }
    },
    deleteCommentFromTheTop(index) {
      this.allcomments.splice(index, 1);
    },
  },
};
</script>

<style></style>
