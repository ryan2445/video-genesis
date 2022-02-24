<template>
  <div class="flex flex-col items-center">
    <AuthForm type="signUp" @signUp="onSignUp" />
  </div>
</template>
<script>
export default {
  methods: {
    onSignUp() {
      this.$router.push({
        path: "/auth/confirm",
      })
    },
  },
}
</script>
