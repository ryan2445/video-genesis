<template>
  <v-app>
    <v-app-bar elevation="0" app>
      <AppBar />
    </v-app-bar>
    <v-main>
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

##Testing out github
