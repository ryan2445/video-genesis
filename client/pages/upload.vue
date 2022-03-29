<template>
    <div class="d-flex justify-center">
        <video-form />
    </div>
</template>

<script>
import UploadBox from '../components/UploadBox.vue'
export default {
    components: { UploadBox },
    layout: 'dashboard',
    created() {
        this.$store.commit('app/setRoute', 'Video Upload')
    }
}
</script>

<style scoped></style>
