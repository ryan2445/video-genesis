<template>
	<div
		class="
			flex flex-col
			justify-center
			bg-gray-200
			p-10
			relative
		"
	>
		<v-progress-linear 
			absolute 
			top 
			indeterminate 
			rounded
			:active="uploading" 
		/>
		<div>
			<svg
				width="*"
				height="36"
				viewBox="0 0 36 36"
				class="upload-label-icon"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<path
					d="M35.4939 14.9112L35.4845 14.8737L30.2252 1.50962C29.9908 0.754931 29.2923 0.234619 28.5002 0.234619H7.18141C6.38453 0.234619 5.67672 0.764307 5.45172 1.52837L0.534531 14.7565L0.520469 14.7893L0.511094 14.8268C0.450156 15.0565 0.431406 15.2909 0.464219 15.5206C0.459531 15.5956 0.454844 15.6706 0.454844 15.7456V32.8971C0.456083 33.6526 0.756748 34.3768 1.29096 34.911C1.82517 35.4452 2.54936 35.7459 3.30484 35.7471H32.7048C34.2752 35.7471 35.5548 34.4674 35.5595 32.8971V15.7456C35.5595 15.6846 35.5595 15.6237 35.5548 15.5721C35.5736 15.3424 35.5548 15.1221 35.4939 14.9112ZM21.6283 12.8956L21.6142 13.6315C21.5767 15.7362 20.1236 17.1518 18.0002 17.1518C16.9642 17.1518 16.0736 16.819 15.4314 16.1862C14.7892 15.5534 14.4377 14.6721 14.4189 13.6315L14.4048 12.8956H4.75797L8.48453 3.83462H27.197L31.0267 12.8956H21.6283ZM4.05016 16.4956H11.4236C12.5627 19.1721 14.9861 20.7518 18.0048 20.7518C19.5845 20.7518 21.0517 20.3112 22.2377 19.4768C23.2783 18.7456 24.0892 17.7237 24.6142 16.4956H31.9502V32.1471H4.05016V16.4956Z"
					fill="#FF7A45"
				/>
			</svg>
		</div>

		<div>
			<v-file-input
				id="video-file-upload-input"
				label="Upload video"
				@change="onFileInputChange"
				show-size
				:loading="uploading"
				style="width:300px"
			>
			</v-file-input>
		</div>

		<div class="flex flex-grow justify-center">
			<v-btn @click="onUpload" :disabled="!video"> 
				Upload
			</v-btn>
		</div>

		<div>
			<p>
				<small class="secondary-text">Support for a single file upload</small>
			</p>
		</div>
		<router-link to="/Description">Description</router-link>
	</div>
</template>

<script>
import UploadDescription from "../components/UploadDescription.vue";
import { PutObjectCommand } from "@aws-sdk/client-s3";
import { nanoid } from "nanoid";
export default {
	components: { UploadDescription },
	layout: "dashboard",
	data() {
		return {
			video: null,

			uploading: false,

			uploadProgress: 0,
		};
	},
	methods: {
		onFileInputChange(file) {
			this.video = file;
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
			}

			// Indicate that we are uploading the video
			this.uploading = true;

			// Generate a key for the payload (this will be the file name)
			const key = encodeURIComponent(this.video.name) + nanoid();

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
			} catch (err) {
				alert("there was an error uploading your video, check the logs");
				console.log(err);
			}

			this.uploading = false;
		},
	},
};
</script>

<style scoped>
</style>