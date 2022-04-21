<template>
  <div class="project-bg mt-24">
    <div class="container">
      <v-row align="center" justify="center">
        <v-col cols="8" class="text-center mt-20 white--text">
          <h4 class="text-4xl mb-8 font-medium">Project Demo</h4>
          <video class="mb-32" controls>
            <source type="video/mp4" src="@/assets/videos/FinalVersion.mp4" />
          </video>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<style scoped>
.project-bg {
  background: center/100% #240e1e;
}
.container {
  margin: auto;
  width: 90%;
}
</style>
