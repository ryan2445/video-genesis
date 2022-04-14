<template>
    <div class="relative" :class="{'cursor-default' : !processed}" :style="`height: ${height}px; width: ${width}px;`"
        @click.prevent="onClick">
        <v-progress-linear absolute top indeterminate
            :active="(play) && !videoCanPlay" />
        <video ref="videoRef" v-show="processed && videoCanPlay && play"
            :controls="false" height="100%" width="100%" loop autoplay muted
            @play="onPlay" @pause="onPause" @canplay="onCanPlay" :src="videoSrc"
            class="object-cover w-full h-full" />
        <img v-if="processed && (!videoCanPlay || (!play && !thumbnailError))"
            alt="Video Thumbnail" :src="thumbnailLink"
            class="w-full h-full object-cover" @load="onThumbnailLoad"
            @error="onThumbnailError" />
        <alternate-video-thumbnail
            v-else-if="!processed || !videoCanPlay || (!play && thumbnailError)"
            :processed="processed" />
        <div v-if="processed && videoCanPlay && (play)"
            class="absolute bottom-2 left-3 z-50">
            <div class="px-1" style="background: rgba(29, 29, 29, 0.5);">
                <span class="text-white" style="font-size:12px;">
                    {{ readableCurrentTime }} / {{ readableDuration }}
                </span>
            </div>
        </div>
        <v-progress-linear absolute bottom :active="videoCanPlay && (play)"
            color="orange" :height="6" :value="videoProgress" />
    </div>
</template>

<script>
export default {
    name: 'VideoThumbnail',
    emits: ['video:loaded', 'click', 'videoTimeChange', 'thumbnail:loaded'],
    props: {
        video: {
            type: Object,
            required: true
        },
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
        },
        height: {
            type: String | Number,
            required: false,
            default: '280'
        },
        width: {
            type: String | Number,
            required: false,
            default: '340'
        },
        processed: {
            type: Boolean,
            required: true,
        }
    },
    data() {
        return {
            videoCanPlay: false,
            playing: false,
            currentTime: 0,
            thumbnailTime: 0,
            duration: 10e9,
            thumbnailError: false,

            // True if the video has played at least once
            playedAtLeastOnce: false
        }
    },
    methods: {
        onCanPlay($event) {
            this.videoCanPlay = true

            this.$emit('video:loaded')

            const video = this.$refs.videoRef

            if (!video) return

            this.duration = video.duration

            // This error occurs whenever the image cannot be loaded due to an invalid link
            if (this.thumbnailError) {
                this.onThumbnailLoad()
            }
        },
        onClick() {
            if (!this.processed) return
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
            const time = videoEl.currentTime

            // Set the current time
            this.currentTime = time

            // Emit the videoTimeChange event with the current time
            this.$emit('videoTimeChange', time)

            setTimeout(this.getCurrentTime, 50)
        },
        onThumbnailLoad() {
            this.$emit('thumbnail:loaded')
        },
        onThumbnailError() {
            this.thumbnailError = true

            this.waitForVideoLoad()
        },
        waitForVideoLoad() {
            if (!this.videoCanPlay) setTimeout(this.waitForVideoLoad, 30)
            else this.loadVideoForThumbnail()
        },
        loadVideoForThumbnail() {
            const video = this.$refs.videoRef

            if (!video) return

            this.thumbnailTime = video.currentTime * 0.1

            video.currentTime = this.thumbnailTime

            video.pause()
        }
    },
    computed: {
        thumbnailLink() {
            if (this.thumbnailSrc) return this.thumbnailSrc
            if (this.video.altThumbnails && this.video.altThumbnails.length > 0) {
                const l = this.video.altThumbnails.length
                const index = l > 3 ? 3 : l > 2 ? 2 : l > 1 ? 1 : 0

                return `https://videogenesis-thumbnails.s3.us-west-2.amazonaws.com/${this.videoKey}/${this.video.altThumbnails[index]}`
            }
            return null
        },
        videoProgress() {
            return (this.currentTime / this.duration) * 100
        },
        readableCurrentTime() {
            if (this.currentTime == null) return '00:00'

            let time = new Date(this.currentTime * 1000).toISOString().substr(11, 8)

            if (time.at(0) == '0' && time.at(1) == '0') {
                return time.substr(3)
            }

            return time
        },
        readableDuration() {
            if (this.duration == null) return '00:00'

            let time = new Date(this.duration * 1000).toISOString().substr(11, 8)

            if (time.at(0) == '0' && time.at(1) == '0') {
                return time.substr(3)
            }

            return time
        }
    },
    watch: {
        play(isPlay) {
            const video = this.$refs.videoRef

            if (!video) return

            if (isPlay) {
                if (!video.playedAtLeastOnce) {
                    this.playedAtLeastOnce = true
                    this.currentTime = 0
                } else {
                    video.currentTime = currentTime
                }

                video.play()
            } else {
                if (this.thumbnailError) video.currentTime = this.thumbnailTime

                video.pause()
            }
        }
    }
}
</script>