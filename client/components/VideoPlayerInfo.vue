<template>
  <v-card>
    <v-card-title class="padding-title">
      <v-row>
        <v-col>
          {{ video.videoTitle }}
        </v-col>
        <div class="flex flex-row justify-end gap-x-10">
          <video-votes :video="video" />
          <save-to-playlist :video="video" class="self-center pt-1" />
        </div>
      </v-row>
    </v-card-title>
    <v-card-text class="padding-text">
      <v-row no-gutters align="center" class="mx-0">
        <v-col class="pa-0">
          <div class="flex flex-row items-center">
            <img
              class="h-10 w-10 object-cover rounded-full"
              :src="video.user.profilePicKey"
              alt="avatar"
              style="border: solid 1px #e1e1e1"
            />
            <div class="flex flex-col self-center pl-2">
              <span class="mr-1 justify-self-end font-bold text-black -mb-1">{{
                owner
              }}</span>
              <span class="text-xs">Nov 13, 2021</span>
            </div>
          </div>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-text v-if="video.videoDescription">
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
  padding-bottom: 8px;
  padding-top: 8px;
  padding-left: 8px;
  padding-right: 8px;
}
.padding-text {
  padding-bottom: 10px;
  padding-top: 10px;
  padding-left: 10px;
  padding-right: 10px;
}
</style>
