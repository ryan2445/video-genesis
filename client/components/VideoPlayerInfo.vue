<template>
  <v-card>
    <v-card-title> {{ video.videoTitle }} </v-card-title>
    <v-card-text>
      <v-row align="center" class="mx-0">
        <div class="mr-2">UserName</div>
        <div class="mr-2">-</div>
        <div>Nov 13, 2021</div>
      </v-row>
    </v-card-text>
    <v-card-text>
      <v-row>
        <v-col cols="8">
          <div class="text-black font-bold">Description:</div>
          <div>{{ video.videoDescription }}</div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: "VideoPlayerInfo",
  props: ["video"],
};
</script>

<style></style>
