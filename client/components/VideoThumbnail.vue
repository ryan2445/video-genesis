<template>
    <v-hover 
        v-slot="{ hover }"
    >
        <div
            class="relative"
            style="height: 280px; width: 380px;"
        >
            <v-progress-linear
                absolute
                top
                indeterminate
                :active="hover && !videoCanPlay"
            />
            <video
                v-show="hover && videoCanPlay"
                :controls="false"
                height="100%"
                width="100%"
                loop
                autoplay
                muted
                @canplay="onCanPlay"
                :src="videoSrc"
                class="object-cover w-full h-full"
            />
            <img
                v-show="!hover || !videoCanPlay"
                alt="Video Thumbnail"
                :src="thumbnailLink"
                class="w-full h-full object-cover"
            />
        </div>
    </v-hover>
</template>

<script>
export default {
    name: "VideoThumbnail",
    props: {
        // The source url of the video (for preview)
        videoSrc: {
            type: String,
            required: false,
            default: null
        },
        // The source url of a thumbnail
        thumbnailSrc: {
            type: String,
            required: false,
            default: null
        },
        // The link of the url
        link: {
            type: String,
            required: false,
            default: null
        },
        videoKey: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            videoCanPlay: false
        }
    },
    methods: {
        onCanPlay($event) {
            this.videoCanPlay = true
        }
    },
    computed: {
        thumbnailLink() {
            return this.thumbnailSrc || `https://videogenesis-thumbnails.s3.us-west-2.amazonaws.com/${this.videoKey}/${this.videoKey}Thumbnails.0000000.jpg`
        }
    }
}
</script>