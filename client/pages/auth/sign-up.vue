<template>
  <div class="flex flex-col contents-center">
    <div class="flex flex-row justify-left items-center">
      <div class="w-3/4 fix-height bg-gray-500">
        <img
          id="image0_29_21383"
          class="object-cover object-bottom bg-gray-700 w-full h-full"
          src="../../assets/images/mountain2.png"
        />
      </div>
      <AuthForm type="signUp" @signUp="onSignUp" />
    </div>
  </div>
</template>
<script>
export default {
  methods: {
    onSignUp() {
      this.$router.push({
        path: "/auth/confirm",
      });
    },
  },
};
</script>

<style scoped>
.fix-height {
  height: 100vh;
}
</style>
