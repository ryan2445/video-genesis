<template>
    <div class="flex w-full justify-center items-center flex-col">
        <!-- Upload Section -->
        <input
            id="file-input"
            type="file"
            name="name"
            style="display: none"
            accept=".png, .jpg, .jpeg"
            @change="profilePicSelected"
        />
        <input
            id="file-input2"
            type="file"
            name="name"
            style="display: none"
            accept=".png, .jpg, .jpeg"
            @change="coverPicSelected"
        />

        <!-- User Profile Pic -->
        <div class="flex flex-row justify-center items-center">
            <div class="mb-4 my-4">
                <div
                    v-if="userProfilePic && !loading"
                    class="w-32 h-32 rounded-full overflow-hidden mb-2"
                >
                    <img
                        class="min-w-full min-h-full object-cover"
                        :src="userProfilePic"
                        alt="avatar"
                    />
                </div>
                <div v-else class="w-32 h-32 rounded-full overflow-hidden mb-2 bg-gray-500">
                    <h1 class="text-center py-12 text-xl font-bold text-white">Upload</h1>
                </div>
                <v-btn
                    :loading="loadingProfilePic"
                    small
                    color="orange lighten-1"
                    class="white--text"
                    @click="uploadProfilePic"
                >
                    <div class="flex flex-row items-center">
                        <v-icon small class="mr-2">mdi-cloud-upload</v-icon>
                        <span
                            >{{ userProfilePic && !loading ? "Change" : "Upload" }} Profile
                            Pic</span
                        >
                    </div>
                </v-btn>
            </div>
            <!--
            User Cover Pic
            <div class="mb-4">
                <div
                    v-if="userCoverPic && !loading"
                    class="h-36 overflow-hidden mb-2 bg-gray-500"
                >
                    <img
                        class="min-w-full min-h-full object-cover"
                        :src="userCoverPic"
                        alt="bird"
                    />
                </div>
                <div v-else class="h-36 overflow-hidden mb-2 bg-gray-500">
                    <h1 class="text-center py-14 text-2xl font-bold text-white">Upload</h1>
                </div>
                <v-btn
                    :loading="loadingCoverPic"
                    small
                    color="orange lighten-1"
                    class="white--text"
                    @click="uploadCoverPic"
                >
                    <div class="flex flex-row items-center">
                        <v-icon small class="mr-2">mdi-cloud-upload</v-icon>
                        <span>
                            {{ userCoverPic && !loading ? "Change" : "Upload" }} Cover Pic
                        </span>
                    </div>
                </v-btn>
            </div>
            -->
        </div>

        <!-- End of Upload Section -->
        <template>
            <v-card class="p-2 w-1/2">
                <v-container fluid>
                    <v-row>
                        <v-col cols="12" sm="6">
                            <v-text-field
                                label="First Name"
                                v-model="usersFirstName"
                                color="orange"
                                required
                                filled
                                rows="2"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <v-text-field
                                label="Last Name"
                                v-model="usersLastName"
                                color="orange"
                                required
                                filled
                                rows="2"
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12">
                            <v-textarea
                                label="About Me"
                                v-model="usersAboutMe"
                                color="orange"
                                filled
                            >
                            </v-textarea>
                        </v-col>
                        <v-card-actions>
                            <v-btn class="mr-2" text @click="resetForm"> Cancel </v-btn>
                            <v-spacer></v-spacer>
                            <v-btn
                                right
                                color="orange"
                                class="white--text"
                                :loading="loading"
                                @click="submit()"
                                >Update</v-btn
                            >
                        </v-card-actions>
                    </v-row>
                </v-container>
            </v-card>
        </template>
    </div>
</template>
<script>
import { mapGetters } from "vuex"
import { nanoid } from "nanoid"
import { PutObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3"
export default {
    layout: "dashboard",
    name: "account",
    data() {
        return {
            usersAboutMe: null,
            usersFirstName: null,
            usersLastName: null,
            profilePicKey: null,
            coverPicKey: null,

            loadingCoverPic: false,
            loadingProfilePic: false,
            loading: true,
        }
    },
    computed: {
        ...mapGetters({
            user: "users/rootUser"
        }),
        userProfilePic() {
            if (!this.user) return null
            return this.profilePicKey || this.user.profilePicKey
        },
        userCoverPic() {
            if (!this.user) return null

            return this.coverPicKey || this.user.coverPicKey
        }
    },
    async mounted() {
        if (!this.user) await this.$store.dispatch("users/userGet")

        this.usersFirstName = this.user.usersFirstName
        this.usersLastName = this.user.usersLastName
        this.usersAboutMe = this.user.usersAboutMe

        this.loading = false
    },

    methods: {
        uploadProfilePic() {
            document.getElementById("file-input").click()
        },
        uploadCoverPic() {
            document.getElementById("file-input2").click()
        },
        async profilePicSelected(event) {
            const file = event.target.files[0]
            const typeArr = file.type.split("/")
            this.loadingProfilePic = true
            try {
                if (this.user.profilePicKey) {
                    const urlArr = this.user.profilePicKey.split("/")
                    const deleteKey = urlArr[urlArr.length - 1]

                    const deletePayload = {
                        Bucket: "videogenesis-profilepics",
                        Key: deleteKey
                    }
                    const deleteCommand = new DeleteObjectCommand(deletePayload)
                    const deleteResp = await this.$store.getters["auth/s3"].send(
                        deleteCommand
                    )
                }
                const putPayload = {
                    Bucket: "videogenesis-profilepics",
                    Key: nanoid() + `.${typeArr[typeArr.length - 1]}`,
                    Body: file,
                    CacheControl: "max-age=31536000"
                }

                const putCommand = new PutObjectCommand(putPayload)

                const putResp = await this.$store.getters["auth/s3"].send(putCommand)
                this.profilepic = `https://videogenesis-profilepics.s3.us-west-2.amazonaws.com/${putPayload.Key}`
            } catch (error) {
                console.error(error)
            }
            this.loadingProfilePic = false
            this.submit()
        },
        async coverPicSelected(event) {
            const file = event.target.files[0]
            const typeArr = file.type.split("/")
            this.loadingCoverPic = true
            try {
                if (this.user.coverPicKey) {
                    const urlArr = this.user.coverPicKey.split("/")
                    const deleteKey = urlArr[urlArr.length - 1]

                    const deletePayload = {
                        Bucket: "videogenesis-profilepics",
                        Key: deleteKey
                    }
                    const deleteCommand = new DeleteObjectCommand(deletePayload)
                    const deleteResp = await this.$store.getters["auth/s3"].send(
                        deleteCommand
                    )
                }
                const putPayload = {
                    Bucket: "videogenesis-profilepics",
                    Key: nanoid() + `.${typeArr[typeArr.length - 1]}`,
                    Body: file,
                    CacheControl: "max-age=31536000"
                }

                const putCommand = new PutObjectCommand(putPayload)

                const putResp = await this.$store.getters["auth/s3"].send(putCommand)
                this.coverPicKey = `https://videogenesis-profilepics.s3.us-west-2.amazonaws.com/${putPayload.Key}`
            } catch (error) {
                console.error(error)
            }
            this.loadingCoverPic = false
            this.submit()
        },

        // if user tries to cancel after they update, it will bring back the old values so call "users/userGet"
        // so the values in the data store get updated
        async resetForm() {
            await this.$store.dispatch("users/userGet")
            this.usersAboutMe = this.user.usersAboutMe
            this.usersFirstName = this.user.usersFirstName
            this.usersLastName = this.user.usersLastName
        },
        async submit() {
            this.loading = true

            const payload = {
                usersFirstName: this.usersFirstName,
                usersLastName: this.usersLastName,
                usersAboutMe: this.usersAboutMe,
                profilePicKey: this.profilePicKey,
                coverPicKey: this.coverPicKey
            }

            const response = await this.$store.dispatch("users/userPut", payload)

            this.$store.commit('users/rootUserSet', {
                ...this.user,
                ...payload
            })

            this.loading = false

            if (!response) return

            return true
        }
    }
}
</script>

<style scoped></style>
