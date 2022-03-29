<template>
  <v-app>
    <TopBar />
    <SideBar />
    <v-main style="background-color:#f0f2f5; padding-top:44px;">
      <div class="ma-8">
        <Nuxt />
      </div>
    </v-main>
  </v-app>
</template>

<script>
export default {
  created() {
    const getS3 = () => {
      this.$store.dispatch('auth/inits3', this.$auth)
    }
    window.mitt.on('SIGN_IN', getS3())
    window.mitt.on('TOKEN_REFRESH', getS3())
    this.$store.dispatch('sr/checkServer')
  }
}
</script>
