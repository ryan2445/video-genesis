<template>
    <v-row justify="space-between" align="center" no-gutters>
        <v-col cols="4">
            <NuxtLink :to="$route.path == '/' ? '/home' : '/'">
                <h1 class="font-medium text-xl mx-4">Video Genesis</h1>
            </NuxtLink>
        </v-col>
        <v-col align="end" cols="8">
            <div v-if="!user">
                <v-btn color="#FF7A45" outlined class="m-2" @click="onSignUp">
                    Sign Up
                </v-btn>
                <v-btn class="white--text" color="orange accent-3" @click="onSignIn">
                    Sign In
                </v-btn>
            </div>
            <div v-else class="flex flex-row items-center" style="justify-content: end">
                <div class="mx-3" v-if="user">
                    <h1>Logged in as {{ user.username }}</h1>
                </div>
                <v-btn v-if="user" @click="onSignOut"> Sign Out </v-btn>
            </div>
        </v-col>
    </v-row>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
    name: 'AppBar',
    methods: {
        onSignUp() {
            this.$router.push({
                path: '/auth/sign-up'
            })
        },
        onSignIn() {
            this.$router.push({
                path: '/auth/sign-in'
            })
        },
        async onSignOut() {
            try {
                await this.$auth.signOut()

                this.$store.commit('users/rootUserSet', null)
                this.$store.commit('auth/clearToken')
                this.$router.push('/')
            } catch (error) {
                console.log('error signing out: ', error)
            }
        }
    },
    computed: {
        ...mapGetters({
            user: 'users/rootUser'
        })
    }
}
</script>
