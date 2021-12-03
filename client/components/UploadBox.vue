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
		<div class="mb-3">
			<svg width="*" height="36" viewBox="0 0 36 36" class="prefix__upload-label-icon" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M35.494 14.911l-.01-.037L30.225 1.51A1.81 1.81 0 0028.5.235H7.181c-.796 0-1.504.53-1.73 1.293L.536 14.757l-.015.032-.009.038c-.06.23-.08.464-.047.694a3.61 3.61 0 00-.01.225v17.151a2.855 2.855 0 002.85 2.85h29.4c1.571 0 2.85-1.28 2.855-2.85V15.746c0-.061 0-.122-.004-.174.019-.23 0-.45-.061-.66zm-13.866-2.015l-.014.736c-.037 2.104-1.49 3.52-3.614 3.52-1.036 0-1.926-.333-2.569-.966-.642-.633-.993-1.514-1.012-2.554l-.014-.736H4.758l3.727-9.061h18.712l3.83 9.06h-9.399zm-17.578 3.6h7.374c1.139 2.676 3.562 4.256 6.58 4.256 1.58 0 3.048-.44 4.234-1.275 1.04-.731 1.851-1.753 2.376-2.981h7.336v15.651H4.05V16.496z" fill="#FF7A45"/></svg>
		</div>
		<div>
			<v-file-input
				id="video-file-upload-input"
				label="Upload video"
				@change="onFileInputChange"
				show-size
				:loading="uploading"
				filled
				hint="Support for a single file upload"
			>
			</v-file-input>
		</div>
	</div>
</template>

<script>
import UploadDescription from "../components/UploadDescription.vue";

export default {
	components: { UploadDescription },
	layout: "dashboard",
	data() {
		return {
			video: null,

			uploading: false,
		};
	},
	mounted() {
	},
	methods: {
		onFileInputChange(file) {
			this.video = file;

			this.$emit('update', file)
		},
	}
};
</script>

<style scoped>
</style>