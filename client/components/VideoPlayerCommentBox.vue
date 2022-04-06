<template>
  <div>
    <div class="h-20 flex flex-row mb-4 mt-2 items-center">
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
      <v-btn class="mr-2" outlined small color="#FF7A45">
        <v-icon class="p-1" center> mdi-minus </v-icon>
      </v-btn>
      <v-btn outlined small color="#FF7A45">
        <v-icon class="p-1" center> mdi-pencil </v-icon>
      </v-btn>
    </div>
  </div>
</template>

<script>
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
};
</script>

<style></style>
