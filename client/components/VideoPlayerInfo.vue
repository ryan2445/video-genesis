<template>
    <v-card>
        <v-card-title> {{ video.videoTitle }} </v-card-title>
        <v-card-text>
            <v-row no-gutters align="end" justify="end" class="mx-0">
                <v-col class="pa-0">
                    <span class="mr-1">{{ owner }}</span>
                    <span class="mr-1">-</span>
                    <span>Nov 13, 2021</span>
                </v-col>
                <v-col>
                    <video-votes :video="video" />
                </v-col>
                <save-to-playlist 
                    :video="video"
                />
            </v-row>
        </v-card-text>
        <v-card-text>
            <v-row>
                <v-col cols="8">
                    <div class="text-black font-bold">Description:</div>
                    <div>{{ video.videoDescription }}</div>
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
export default {
    props: {
        video: {
            type: Object,
            required: true
        }
    },
    computed: {
        owner() {
            return this.video.pk.substr(3)
        }
    }
}
</script>

<style></style>
