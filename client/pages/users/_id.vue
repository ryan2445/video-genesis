<template>
    <user-profile v-if="user" :user="user" />
</template>

<script>
import { mapGetters } from 'vuex'
export default {
    name: 'UserProfilePage',
    layout: 'dashboard',
    data() {
        return {
            tabSelected: 'Uploads',
            loading: true,
            username: '',
            videos: []
        }
    },
    methods: {
        changeTabSelection(tabName) {
            this.tabSelected = tabName
        },
        getQueryParamsAndSetKeys() {
            const path = this.$route.fullPath.replace('/users/', '')
            const params = new URLSearchParams(path)

            // If the username is not provided, error
            if (!params.has('username')) {
                return
            }

            const username = params.get('username')
            this.username = username
        }
    },
    async mounted() {
        this.getQueryParamsAndSetKeys()
        
        const user = await this.$store.dispatch('users/userGetByUsername', this.username)

        this.$store.commit('users/selectedUserSet', user)

        this.$store.commit('app/setRoute', user.username)

        this.loading = false
    },
    computed: {
        ...mapGetters({
            'user': 'users/selectedUser'
        })
    }

}
</script>

<style scoped>
.v-enter-active,
.v-leave-active {
    transition: opacity 0.5s ease;
}

.v-enter-from,
.v-leave-to {
    opacity: 0;
}
</style>
