<template>
  <div class="flex flex-col contents-center">
    <div class="flex flex-row justify-left items-center">
      <div class="w-3/4 fix-height">
        <img
          id="image0_29_21383"
          class="object-cover object-bottom bg-gray-700 w-full h-full"
          src="../../assets/images/mountain1.png"
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
