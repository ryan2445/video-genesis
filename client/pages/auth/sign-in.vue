<template>
  <div class="flex flex-col contents-center">
    <div class="flex flex-row justify-left items-center">
      <div class="w-3/4 fix-height">
        <img
          id="image0_29_21383"
          class="object-cover object-bottom bg-gray-700 w-full h-full"
          src="https://images.unsplash.com/photo-1567650076010-186173332565?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1974&q=80"
        />
      </div>

      <AuthForm type="signIn" @signIn="onSignIn" />
    </div>
  </div>
</template>

<script lang="js">
export default {
    name: "sign-in",
    methods: {
        onSignIn() {
            this.$router.push({
                path: '/home'
            })
        }
    }
}
</script>

<style scoped>
.fix-height {
  height: 100vh;
}
</style>
