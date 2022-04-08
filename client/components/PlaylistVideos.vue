<template>
    <div>
        <v-row v-if="!!playlist.videos" class="justify-center">
            <div v-for="(playlistItem, index) in playlist.videos" :key="index">
                <video-card :video="playlistItem.video" />
            </div>
        </v-row>
    </div>
</template>
<script>
import { mapGetters } from 'vuex'

export default {
    name: 'PlaylistVideos',
    props: {
        playlist: {
            type: Object,
            required: true
        }
    },
    data() {
        return {}
    },

    computed: {
        ...mapGetters({
            user: 'users/rootUser'
        })
    },
    async mounted() {}
}
</script>
