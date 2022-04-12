<template>
  <v-app>
    <TopBar />

    <SideBar />

    <v-main style="background-color: #f0f2f5">
      <v-container
        fluid
        style="padding-left: 0px; padding-right: 0px; padding-top: 0px"
      >
        <div class="flex w-full justify-center items-center">
          <div style="max-width: 1420px; width: 100%">
            <Nuxt />
          </div>
        </div>
      </v-container>
    </v-main>
    <notifications position="bottom right" />
  </v-app>
</template>

<script>
export default {
  created() {
    const getS3 = () => {
      this.$store.dispatch("auth/inits3");
    };
    window.mitt.on("SIGN_IN", getS3());
    window.mitt.on("TOKEN_REFRESH", getS3());
    this.$store.dispatch("sr/checkServer");
  }
};
</script>