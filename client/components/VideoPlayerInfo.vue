<template>
  <v-card>
    <v-card-title>
      <v-row>
        <v-col>
          {{ video.videoTitle }}
        </v-col>
        <div class="flex flex-row justify-end gap-x-10">
          <video-votes :video="video" />
          <save-to-playlist :video="video" class="self-center" />
        </div>
      </v-row>
    </v-card-title>
    <v-card-text class="padding-text">
      <v-row no-gutters align="center" class="mx-0">
        <v-col class="pa-0">
          <span class="mr-1">{{ owner }}</span>
          <span class="mr-1">-</span>
          <span>Nov 13, 2021</span>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-text>
      <v-row>
        <v-col cols="8" class="">
          <div class="text-black font-bold">Description:</div>
          <div>{{ video.videoDescription }}</div>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>
<script>
export default {
  props: {
    video: {
      type: Object,
      required: true,
    },
  },
  computed: {
    owner() {
      return this.video.pk.substr(3);
    },
  },
};
</script>

<style>
.padding-title {
  padding-bottom: 0px;
  padding-top: 8px;
}
.padding-text {
  padding-bottom: 0px;
}
</style>
