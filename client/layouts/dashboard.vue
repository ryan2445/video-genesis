<template>
  <v-app>
    <TopBar />
    <SideBar />
    <v-main style="background-color: #f0f2f5; padding-top: 44px;">
      <v-container fluid>
        <div class="flex justify-center items-center w-full h-full">
          <div style="width: 1280px;">
            <Nuxt />
          </div>
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  created() {
    const getS3 = () => { this.$store.dispatch('auth/inits3', this.$auth) }
    window.mitt.on('SIGN_IN', getS3());
    window.mitt.on('TOKEN_REFRESH', getS3());
    this.$store.dispatch('sr/checkServer')
  },
}
</script>
