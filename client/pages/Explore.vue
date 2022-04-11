<template>
    <div>
        <div v-if="loading" class="text-center" style="height: 100vh">
            <v-progress-circular indeterminate color="orange" style="top: 50%" />
        </div>
        <div
            v-if="!loading && videos && !videos.length"
            class="text-center"
            style="
            display: flex;
            height: 50vh;
            align-items: center;
            justify-content: center;
        "
        >
            <div>No videos found</div>
        </div>
        <explore-top @search="searchText = $event, paginate()" />
        <video-list  class="bg-white rounded-md px-4 py-2" :videos="videosOnCurrentPage || []" />
        <div class="text-xs-center">
            <v-pagination
                color="orange"
                v-model="page"
                :length="paginationLength"
                @input="paginate"
            ></v-pagination>
        </div>
    </div>
    <!-- <VideoList /> -->
</template>
<script>
import { mapGetters } from 'vuex'
import VideoCard from '../components/VideoCard.vue'
export default {
    components: { VideoCard },
    layout: 'dashboard',
    name: 'Explore',
    data() {
        return {
            //  Controls v-progress-circular
            loading: true,
            page: 1,
            videosOnCurrentPage: null,
            videosPerPage: 8,
            paginationLength: null,
            searchText: null
        }
    },
    created() {
        this.$store.commit('app/setRoute', 'Explore')
    },
    async mounted() {
        //  Send request to get videos
        await this.$store.dispatch('videos/getAllVideos')

        //  Stop loading
        this.loading = false
        this.paginationLength = Math.ceil(this.videos.length / this.videosPerPage)
        if (this.videos.length > this.videosPerPage) {
            this.videosOnCurrentPage = this.videos.slice(0, this.videosPerPage)
        } else {
            this.videosOnCurrentPage = this.videos.slice(0, this.videos.length)
        }
    },
    computed: {
        ...mapGetters({
            videos: 'videos/videos'
        })
    },
    methods: {
        async paginate(pageNumber = 1) {
            let videos = this.videos
            let startingIndex = 0
            let lastIndex = 0
            startingIndex = (pageNumber - 1) * this.videosPerPage
            lastIndex = startingIndex + this.videosPerPage

            if (this.searchText) videos = videos.filter(this.matchesSearchText)

            if (this.videos.length < lastIndex) lastIndex = videos.length

            this.videosOnCurrentPage = videos.slice(startingIndex, lastIndex)
        },
        matchesSearchText(video) {
            const searchText = this.searchText.toLowerCase()

            return (
                video.videoTitle.toLowerCase().includes(searchText) ||
                (video.videoDescription &&
                    video.videoDescription.toLowerCase().includes(searchText)) ||
                (video.user &&
                    (video.user.username.toLowerCase().includes(searchText) ||
                        (video.user.usersFirstName &&
                            video.user.usersFirstName
                                .toLowerCase()
                                .includes(searchText)) ||
                        (video.user.usersLastName &&
                            video.user.usersLastName.toLowerCase().includes(searchText))))
            )
        }
    }
}
</script>

<style scoped></style>
