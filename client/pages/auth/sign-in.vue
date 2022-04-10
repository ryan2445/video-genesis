<template>
  <div class="flex flex-col contents-center">
    <div class="flex flex-row justify-left items-center">
      <div class="w-3/4 fix-height bg-gray-500">
        <!-- <svg
          width="999"
          height="800"
          viewBox="0 0 1230 1024"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          xmlns:xlink="http://www.w3.org/1999/xlink"
        >
          <rect width="2000" height="1036" fill="#FFF2E8" />
          <rect width="2000" height="1036" fill="url(#pattern0)" />
          <defs>
            <pattern
              id="pattern0"
              patternContentUnits="objectBoundingBox"
              width="1"
              height="1"
            >
              <use
                xlink:href="#image0_29_21383"
                transform="translate(-0.22549) scale(0.00070028)"
              />
            </pattern>
           
          </defs>
        </svg> -->
        <img
          id="image0_29_21383"
          class="object-cover object-bottom bg-gray-700 w-full h-full"
          src="https://images.unsplash.com/photo-1567650076010-186173332565?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1974&q=80"
        />
      </div>
      <div class="fix-height">
        <div class="mt-56">
          <AuthForm type="signIn" @signIn="onSignIn" />
        </div>
      </div>
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
  height: calc(100vh - 64px);
}
</style>
