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
                ref="videoRef"
                v-show="videoCanPlay && (hover || play)"
                :controls="false"
                height="100%"
                width="100%"
                loop
                autoplay
                muted
                @play="onPlay"
                @pause="onPause"
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
            videoCanPlay: false,
            playing: false,
            currentTime: 0
        }
    },
    methods: {
        onCanPlay($event) {
            this.videoCanPlay = true
        },
        onClick() {
            this.$emit('click')
        },
        onPlay() {
            this.playing = true
            this.getCurrentTime()
        },
        onPause() {
            this.playing = false
        },
        getCurrentTime() {
            if (!this.playing) return
            
            // Get the video element
            const videoEl = this.$refs.videoRef

            // If the video element does not exist, return
            if (!videoEl) return
            
            // Get the current time the video is at
            const time = videoEl.currentTime;
            
            // Set the current time
            this.currentTime = time
            
            // Emit the videoTimeChange event with the current time
            this.$emit('videoTimeChange', time)

            setTimeout(this.getCurrentTime, 50)
        }
    },
    computed: {
        thumbnailLink() {
            return this.thumbnailSrc || `https://videogenesis-thumbnails.s3.us-west-2.amazonaws.com/${this.videoKey}/${this.videoKey}Thumbnails.0000000.jpg`
        }
    }
}
</script>