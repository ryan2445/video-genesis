<template>
    <v-menu offset-y v-model="menuDisplay">
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                :loading="downloading"
                :disabled="downloading"
            >
                <v-icon> mdi-download </v-icon>
            </v-btn>
        </template>
        <v-card>
            <v-card-title> Downloads </v-card-title>
            <v-divider></v-divider>
            <v-list>
                <v-list-item
                    v-for="link of downloadLinks"
                    :key="link.url"
                    @click="download(link)"
                    color="orange"
                >
                    {{ link.title }}
                </v-list-item>
            </v-list>
        </v-card>
    </v-menu>
</template>
<script>
export default {
    props: {
        video: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            menuDisplay: false,
            BUCKET_URL:
                "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com",
            downloading: false
        }
    },
    methods: {
        async download(link) {
            const url = link.url

            const filename = `${link.title}.mp4`

            let downloadElement = document.createElement("a")

            downloadElement.download = filename

            this.downloading = true

            await fetch(url)
                .then(response => response.blob())
                .then(blob => {
                    const blobUrl = window.URL.createObjectURL(blob)
                    downloadElement.href = blobUrl
                })
                .catch(e => console.error(e))

            downloadElement.click()

            this.downloading = false
        }
    },
    computed: {
        downloadLinks() {
            const links = this.video.videoData.map(data => {
                return {
                    url: `${this.BUCKET_URL}/${this.video.videoKey}/${data.baseURL}`,
                    title: data.width
                }
            })

            links.push({
                url: `${this.BUCKET_URL}/${this.video.videoKey}/${this.video.videoKey}.mp4`,
                title: "audio"
            })

            if (!!this.video.lrBaseURL) {
                links.push({
                    url: `${this.BUCKET_URL}/${this.video.videoKey}/${this.video.lrBaseURL}`,
                    title: "DS"
                })
            }
            if (!!this.video.hrBaseURL) {
                links.push({
                    url: `${this.BUCKET_URL}/${this.video.videoKey}/${this.video.hrBaseURL}`,

                    title: "SR"
                })
            }

            return links
        }
    }
}
</script>
