<template>
  <div>
    <div class="group h-20 flex flex-row mb-4 mt-2 items-center">
      <div class="p-2 mr-2">
        <img
          class="h-14 w-14 object-cover rounded-full"
          :src="user.profilePicKey"
          alt="avatar"
          style="border: solid 1px #e1e1e1"
        />
      </div>
      <!-- main -->
      <div class="flex flex-col">
        <!-- header -->
        <div>
          <h2 class="font-semibold">{{ user.username }}</h2>
        </div>
        <div>{{ comment.content }}</div>
      </div>
      <!-- buttons -->
      <div
        v-if="comment.userId == rootUser.username"
        class="opacity-0 group-hover:opacity-100"
      >
        <v-btn
          class="mr-2"
          @click="deleteComment"
          outlined
          small
          color="#FF7A45"
        >
          <v-icon class="p-1" center> mdi-minus </v-icon>
        </v-btn>

        <v-btn outlined small color="#FF7A45">
          <v-icon class="p-1" center> mdi-pencil </v-icon>
        </v-btn>
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
  computed: {
    ...mapGetters({
      rootUser: "user/user",
    }),
  },
  methods: {
    async deleteComment() {
      try {
        const response = await this.$axios.delete("comments", {
          data: { videoId: this.comment.pk, commentId: this.comment.sk },
        });
        console.log("Why");
        this.$emit("deleteCommentFromTheTop", this.index);
        return response.data;
      } catch (exception) {
        return null;
      }
    },
  },
};
</script>

<style></style>
