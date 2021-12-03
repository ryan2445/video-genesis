<template>
    <v-card
        rounded
        min-width="520"
        
    >
        <v-card-title
            class="bg-gray-300"
        >
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
            @update="onVideoUpdate"
        />
        <div
            class="flex flex-grow justify-center bg-gray-300 py-3"
        >
            <v-btn
                @click="onUpload"
            >
                Upload
            </v-btn>
        </div>
    </v-card>
</template>

<script lang="js">
import { PutObjectCommand } from "@aws-sdk/client-s3";
import { nanoid } from "nanoid";
export default {
    name: "VideoForm",
    props: {
        
    },
    data() {
        return {
            // The title of the video
            title: null,

            // The description of the video
            description: null,

            // The video
            video: null,

            // Determines if we are currently uploading
            uploading: false
        }
    },
    methods: {
        onVideoDescriptionUpdate(object) {
            this.title = object.title
            this.description = object.description
        },
        onUpload(object) {

        },
        async onUpload() {
			// If the video was not set, alert the user
			if (!this.video) {
				alert("Select a video before uploading");
				return;
			} else if (this.video.type !== "video/mp4") {
				alert("mp4 is only supported");
				return;
			} else if (this.video.size > 5.12e8) {
				alert("The file size must be less than 512 megabytes");
				return;
			}

			// Indicate that we are uploading the video
			this.uploading = true;

			// Generate a key for the payload (this will be the file name)
			const key = encodeURIComponent(this.video.name).replace('.mp4', nanoid() + '.mp4')

			// Generate the payload
			const payload = {
				Bucket: "genesis2vod-staging-input-q1h5l756",
				Key: key,
				Body: this.video,
			};

			try {
				// Get the PutObjectCommand for S3
				const command = new PutObjectCommand(payload);

				// Send the PutObject request to S3
				const resp = await this.$s3.send(command);

                // After video is uploaded, post the video to database
                

			} catch (err) {
				alert('error uploading video')
				console.log(err);
			}

			this.uploading = false;
		},
        onVideoUpdate(video) {
            this.video = video
        }
    },
    computed: {

    }
}
</script>