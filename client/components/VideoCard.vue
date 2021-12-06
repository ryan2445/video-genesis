<template>
	<v-container>
		<div>
			<v-card class="mx-auto" outlined>
				<v-row>
					<v-col cols="4">
						<v-img
							height="250"
							src="https://cdn.vuetifyjs.com/images/cards/cooking.png"
						></v-img>
					</v-col>
					<v-col cols="8">
						<v-list-item three-line>
							<v-list-item-content>
								<v-list-item-title class="text-overline mb-4">
									{{ video.videoTitle }}
								</v-list-item-title>
								<v-list-item-subtitle>
									{{ video.videoDescription }}
								</v-list-item-subtitle>
							</v-list-item-content>
						</v-list-item>
					</v-col>
				</v-row>
			</v-card>
			<br />
		</div>
	</v-container>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
	name: 'VideoCard',

	props: {
		video: {
			type: Object,
			required: true
		}
	},
	computed: {
		...mapGetters({
			user: 'user/user'
		})
	}
}
</script>

<style></style>
