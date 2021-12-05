<template>
  <div class="grid place-items-center h-screen"
>
    <home-page />
  </div>
 
</template>

<script>
import HomePage from '../components/HomePage.vue';
export default {
  components: { HomePage },
  layout: "dashboard",
};
</script>

<style scoped>
</style>