<template>
    <div class="d-flex flex-row" style="float: right">
        <div class="d-flex flex-row align-center">
            <div class="mr-1">
                <v-btn icon color="grey darken-2" @click="setVote(true)">
                    <v-icon v-if="liked">mdi-thumb-up</v-icon>
                    <v-icon v-else>mdi-thumb-up-outline</v-icon>
                </v-btn>
            </div>
            <div class="mr-2">
                {{ videoLikes }}
            </div>
        </div>
        <div class="d-flex flex-row align-center">
            <div class="mr-1">
                <v-btn icon color="grey darken-2" @click="setVote(false)">
                    <v-icon v-if="disliked">mdi-thumb-down</v-icon>
                    <v-icon v-else>mdi-thumb-down-outline</v-icon>
                </v-btn>
            </div>
            <div class="mr-2">
                {{ videoDislikes }}
            </div>
        </div>
    </div>
</template>
<script>
import { mapGetters } from "vuex"
import { debounce } from "lodash"
export default {
    props: {
        video: {
            type: Object,
            required: true
        }
    },
    data() {
        return {
            vote: null,
            voteObject: null,
            previousVote: null
        }
    },
    async mounted() {
        await this.getVote()
    },
    computed: {
        ...mapGetters({
            user: "user/user"
        }),
        liked() {
            if (!this.vote === null) return null

            return this.vote === true
        },
        disliked() {
            if (!this.vote === null) return null

            return this.vote === false
        },
        videoLikes: {
            get() {
                if (!this.video) return null

                return this.video.likes || 0
            },
            set(number) {
                this.video.likes = number
            }
        },
        videoDislikes: {
            get() {
                if (!this.video) return null

                return this.video.dislikes || 0
            },
            set(number) {
                this.video.dislikes = number
            }
        }
    },
    methods: {
        async getVote() {
            const response = await this.$store.dispatch("users/usersGetVotes", {
                userId: this.user.username,
                videoId: this.video.sk.split("#")[1]
            })

            this.voteObject = response.vote
            this.vote = response.vote && response.vote.upvoted
            this.previousVote = this.vote
        },
        async setVote(bool) {
            if (bool === true && this.vote === true) {
                this.videoLikes -= 1
                this.vote = null
            } else if (bool === false && this.vote === false) {
                this.videoDislikes -= 1
                this.vote = null
            } else {
                if (bool) this.videoLikes += 1
                else this.videoDislikes += 1

                if (this.vote === false && bool) this.videoDislikes -= 1
                else if (this.vote === true && !bool) this.videoLikes -= 1

                this.vote = bool
            }

            this.saveVote()
        },
        saveVote: debounce(function () {
            if (this.vote == this.previousVote) return

            this.previousVote = this.vote

            this.$store.dispatch("users/usersPostVotes", {
                videoId: this.video.sk.split("#")[1],
                videoUserId: this.video.pk.split("#")[1],
                upvoted: this.vote
            })
        }, 1000)
    }
}
</script>
