<template>
    <div class="mb-1 mt-2 h-max p-1 clear">
        <div class="group flex flex-row items-start">
            <div class="p-1 pr-3">
                <img class="h-14 w-14 object-cover rounded-full" :src="user.profilePicKey"
                    alt="avatar" style="border: solid 1px #e1e1e1" />
            </div>
            <!-- main -->
            <div class="flex flex-row items-center self-center" v-if="!isEditing">
                <div class="flex flex-col">
                    <!-- header -->
                    <div>
                        <h2 class="font-semibold">{{ user.username }}</h2>
                    </div>
                    <div>{{ comment.content }}</div>
                </div>
                <!-- buttons -->
                <div v-if="comment.userId == rootUser.username && !isEditing"
                    class="opacity-0 group-hover:opacity-100 self-start mt-2">
                    <v-btn class="mr-2" @click="deleteComment" small depressed
                        color="error">
                        <v-icon class="p-1" center> mdi-minus </v-icon>
                    </v-btn>

                    <v-btn small depressed @click="isEditing = true" color="#FF7A45">
                        <v-icon class="p-1" color="white" center> mdi-pencil </v-icon>
                    </v-btn>
                </div>
            </div>
            <!-- text-area -->
            <div class="flex flex-col" v-else-if="isEditing">
                <v-textarea auto-grow rows="1" :value="this.comment.content"></v-textarea>
                <!-- buttons -->
                <div class="flex justify-end gap-2 -mt-3">
                    <v-btn @click="isEditing = false" depressed>Cancel</v-btn>
                    <v-btn :disabled="checkTextArea" :loading="isLoading"
                        @click="submitComment" class="white--text" color="#FF7A45"
                        depressed>Update</v-btn>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
    data: () => ({
        isEditing: false
    }),
    props: {
        comment: {
            type: Object,
            required: true
        },
        user: {
            type: Object,
            required: true
        },
        index: {
            type: Number,
            required: true
        }
    },
    computed: {
        ...mapGetters({
            rootUser: 'users/rootUser'
        })
    },
    methods: {
        async deleteComment() {
            try {
                const response = await this.$axios.delete('comments', {
                    data: { videoId: this.comment.pk, commentId: this.comment.sk }
                })
                console.log('Why')
                this.$emit('deleteCommentFromTheTop', this.index)
                return response.data
            } catch (exception) {
                return null
            }
        }
    }
}
</script>

<style></style>
