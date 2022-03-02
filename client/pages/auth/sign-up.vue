<template>
  <div class="flex flex-col">
    <div class="flex justify-center">
      <svg
        width="952"
        height="800"
        viewBox="0 0 952 1024"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
      >
        <rect width="1000" height="1046" fill="#FFF2E8" />
        <rect width="1000" height="1046" fill="url(#pattern0)" />
        <defs>
          <pattern
            id="pattern0"
            patternContentUnits="objectBoundingBox"
            width="1"
            height="1"
          >
            <use
              xlink:href="#image0_29_11522"
              transform="translate(-0.323836) scale(0.000872708)"
            />
          </pattern>
          <image
            id="image0_29_11522"
            width="1888"
            height="1259"
            xlink:href="https://images.unsplash.com/photo-1599551528722-6b6d968512a2?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80"
          />
        </defs>
      </svg>

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
