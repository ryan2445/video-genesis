<template>
    <div>
        <video-card />
    </div>
    <!-- <VideoList /> -->
</template>

<script>
import { mapGetters } from 'vuex'
import VideoCard from '../../components/VideoCard.vue'
export default {
    components: { VideoCard },
    layout: 'dashboard',
    data() {
        return {}
    },
    computed: {
        ...mapGetters({
            user: 'user/user',
            videos: 'videos/videos'
        })
    },
    mounted() {
        this.$store.dispatch('videos/videosGet')
    }
}
</script>

<style scoped></style>
