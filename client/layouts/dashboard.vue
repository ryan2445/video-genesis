<template>
  <v-app>
    <TopBar />
    <SideBar />
    <v-main style="background-color: #f0f2f5">
        <v-container>
        <Nuxt />
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
  },
}
</script>
