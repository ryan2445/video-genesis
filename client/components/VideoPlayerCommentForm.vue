<template>
  <v-card class="mt-2 pd">
    <v-textarea
      v-model="content"
      name="input-7-1"
      filled
      label="Leave a comment"
      auto-grow
      color="orange orange-darken-4"
      rows="3"
    ></v-textarea>
    <div class="p-2 flex justify-end gap-2 -mt-7">
      <v-btn :disable="!form" :loading="isLoading" depressed>Cancel</v-btn>
      <v-btn
        :disable="!form"
        :loading="isLoading"
        class="white--text"
        color="#FF7A45"
        depressed
        >Comment</v-btn
      >
    </div>
  </v-card>
</template>

<script>
import VideoCard from "./VideoCard.vue";
export default {};
</script>

<style></style>
