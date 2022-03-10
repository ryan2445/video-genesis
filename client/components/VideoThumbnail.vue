<template>
    <v-hover 
        v-slot="{ hover }"
        :open-delay="300"
    >
        <div
            class="relative"
            style="height: 280px; width: 380px;"
            @click.prevent="onClick"
        >
            <v-progress-linear
                absolute
                top
                indeterminate
                :active="(hover || play) && !videoCanPlay"
            />
            <video
                v-show="videoCanPlay && (hover || play)"
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
                v-show="!videoCanPlay || (!hover && !play)"
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
        },
        // Plays the video
        play: {
            type: Boolean,
            required: false,
            default: false
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
        },
        onClick() {
            this.$emit('click')
        }
    },
    computed: {
        thumbnailLink() {
            return this.thumbnailSrc || `https://videogenesis-thumbnails.s3.us-west-2.amazonaws.com/${this.videoKey}/${this.videoKey}Thumbnails.0000000.jpg`
        }
    }
}
</script>