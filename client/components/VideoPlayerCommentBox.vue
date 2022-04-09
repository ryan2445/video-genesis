<template>
  <div class="mb-1 mt-2 h-max p-1 clear">
    <div class="group flex flex-row items-start">
      <div class="p-1 pr-3">
        <img
          class="h-14 w-14 object-cover rounded-full"
          :src="user.profilePicKey"
          alt="avatar"
          style="border: solid 1px #e1e1e1"
        />
      </div>
      <!-- main -->
      <div class="flex flex-row items-center self-center" v-if="!isEditing">
        <div class="flex flex-col">
          <!-- header -->
          <div>
            <h2 class="font-semibold">{{ user.username }}</h2>
          </div>
          <div class="whitespace-pre-wrap">
            <span class="line-clamp-4">{{ comment.content }}</span>
          </div>
        </div>
        <!-- buttons -->
        <div
          v-if="comment.userId == rootUser.username && !isEditing"
          class="opacity-0 group-hover:opacity-100 self-start mt-2"
        >
          <v-btn
            class="mr-2"
            @click="deleteComment"
            small
            depressed
            color="error"
          >
            <v-icon class="p-1" center> mdi-minus </v-icon>
          </v-btn>

          <v-btn small depressed @click="changeToEdit()" color="#FF7A45">
            <v-icon class="p-1" color="white" center> mdi-pencil </v-icon>
          </v-btn>
        </div>
      </div>
      <!-- text-area -->
      <div class="flex flex-col" v-else-if="isEditing">
        <v-textarea
          auto-grow
          rows="1"
          v-model="content"
          color="orange orange-darken-4"
          ref="textArea"
        ></v-textarea>
        <!-- buttons -->
        <div class="flex justify-end gap-2 -mt-3">
          <v-btn @click="resetTextArea" text>Cancel</v-btn>
          <v-btn
            :disabled="checkTextArea"
            :loading="isLoading"
            @click="updateComment()"
            class="white--text"
            color="#FF7A45"
            depressed
            >Update</v-btn
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  props: {
    comment: {
      type: Object,
      required: true,
    },
    user: {
      type: Object,
      required: true,
    },
    index: {
      type: Number,
      required: true,
    },
  },
  data: () => ({
    isEditing: false,
    content: "",
    isLoading: false,
  }),
  computed: {
    ...mapGetters({
      rootUser: "users/rootUser",
    }),
    checkTextArea() {
      return !this.content;
    },
  },
  mounted() {
    this.content = this.comment.content;
  },
  methods: {
    changeToEdit() {
      this.content = this.comment.content;
      this.isEditing = true;
      const interval = setInterval(() => {
        if (this.$refs.textArea) {
          this.$refs.textArea.focus();
          clearInterval(interval);
        }
      }, 50);
    },
    resetTextArea() {
      this.isEditing = false;
      this.content = this.comment.content;
    },
    async deleteComment() {
      try {
        const response = await this.$axios.delete("comments", {
          data: { videoId: this.comment.pk, commentId: this.comment.sk },
        });
        this.$emit("deleteCommentWithIndex", this.index);
        return response.data;
      } catch (exception) {
        return null;
      }
    },
    async updateComment() {
      try {
        this.isLoading = true;
        await this.$axios.post("comments", {
          videoId: this.comment.pk,
          commentId: this.comment.sk,
          content: this.content,
        });
        this.isLoading = false;
        this.isEditing = false;
        this.$emit("updateCommentWithIndex", this.index, this.content);
      } catch (exception) {
        return null;
      }
    },
  },
};
</script>

<style></style>
