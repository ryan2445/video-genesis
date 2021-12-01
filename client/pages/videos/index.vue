<template>
  <v-container class="">
    <v-row>
      <v-col>
        <VideoPlayer
          src="https://multiplatform-f.akamaihd.net/i/multi/will/bunny/big_buck_bunny_,640x360_400,640x360_700,640x360_1000,950x540_1500,.f4v.csmil/master.m3u8"
        />
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  layout: "dashboard",
};
</script>

<style scoped></style>
