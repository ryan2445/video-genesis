<template>
  <v-card class="mt-2 pd">
    <v-textarea
      v-model="content"
      name="input-7-1"
      filled
      label="Leave a comment"
      auto-grow
      color="#A13440"
      rows="3"
    ></v-textarea>
    <v-card-actions
      ><div class="p-2 flex justify-end gap-2 -mt-7">
        <v-btn @click="resetTextArea" text>Cancel</v-btn>
        <v-btn
          :disabled="checkTextArea"
          :loading="isLoading"
          @click="submitComment"
          class="white--text"
          color="#A13440"
          depressed
          >Comment</v-btn
        >
      </div></v-card-actions
    >
  </v-card>
</template>

<script>
import VideoCard from "./VideoCard.vue";
export default {
  props: {
    video: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    form: false,
    content: "",
    isLoading: false,
  }),
  computed: {
    checkTextArea() {
      return !this.content;
    },
  },
  methods: {
    resetTextArea() {
      this.content = "";
    },
    async submitComment() {
      try {
        this.isLoading = true;
        console.log(this.video.sk);
        const response = await this.$axios.put("comments", {
          videoId: this.video.sk,
          content: this.content,
        });
      } catch (exception) {
        return null;
      }
      // try {
      //   const response = await this.$axios.put("videos", params);
      //   return response.data;
      // } catch (exception) {
      //   return null;
      // }
      this.isLoading = false;
      this.$emit("addCommentToTheTop");
      this.content = "";
    },
  },
};
</script>

<style></style>
