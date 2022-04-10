<template>
  <div class="flex flex-col contents-center bg-gray-500">
    <div class="flex justify-center">
      <svg
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
          <image
            id="image0_29_21383"
            width="2072"
            height="1554"
            xlink:href="https://images.unsplash.com/photo-1567650076010-186173332565?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1974&q=80"
          />
        </defs>
      </svg>
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
