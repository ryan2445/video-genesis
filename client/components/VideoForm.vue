<template>
    <v-card
        rounded
        min-width="520"
    >
        <v-card-title>
            <div
                class="flex justify-center"
            > 
                <h3>
                    Upload Video
                </h3>
                <v-icon right>
                    icon-video
                </v-icon>
            </div>
            
        </v-card-title>
        <upload-description 
            @update="onVideoDescriptionUpdate" 
        />
        <upload-box 
        
        />
    </v-card>
</template>

<script lang="js">
export default {
    name: "VideoForm",
    props: {
        
    },
    data() {
        return {
            // The title of the video
            title: null,

            // The description of the video
            description: null
        }
    },
    methods: {
        onVideoDescriptionUpdate(object) {
            this.title = object.title
            this.description = object.description
        }
    },
    computed: {

    }
}
</script>