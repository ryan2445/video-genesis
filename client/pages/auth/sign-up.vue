<template>
  <div class="flex flex-col contents-center">
    <div class="flex flex-row justify-left items-center">
      <div class="w-3/4 fix-height bg-gray-500">
        <img
          id="image0_29_21383"
          class="object-cover object-bottom bg-gray-700 w-full h-full"
          src="https://images.unsplash.com/photo-1599551528722-6b6d968512a2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"
        />
      </div>
      <div class="fix-height">
        <div class="mt-56">
          <AuthForm type="signUp" @signUp="onSignUp" />
        </div>
      </div>
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
