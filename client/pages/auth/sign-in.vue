<template>
  <div class="flex flex-col">
    <div class="flex justify-center">
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
