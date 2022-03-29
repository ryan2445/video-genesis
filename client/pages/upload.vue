<template>
    <div class="d-flex justify-center">
        <video-form />
    </div>
</template>
<script>
export default {
    layout: 'dashboard',
    created() {
        this.$store.commit('app/setRoute', 'Video Upload')
    }
}
</script>
<style scoped></style>
