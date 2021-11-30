<template>
  <div class="grid place-items-center h-screen"
>
    <UploadDescription/>
  </div>
 
</template>

<script>
import UploadDescription from '../components/UploadDescription.vue';
export default {
  components: { UploadDescription },
  layout: "dashboard",
};
</script>

<style scoped>
</style>