<template>
    <v-row justify="space-between" align="center" no-gutters>
        <v-col cols="2">
            <h1>
                Video Genesis
            </h1>
        </v-col>
        <v-col cols="10">
            <v-row align="center" justify="end" no-gutters>
                <v-btn
                    v-if="!user"
                    @click="onSignUp"
                >
                    Sign Up
                </v-btn>
                <v-btn
                    v-if="!user"
                    @click="onSignIn"
                >
                    Sign In
                </v-btn>
                <div class="mx-3" v-if="!!user">
                    <h1>
                        Logged in as {{ user.username }}
                    </h1>
                </div>
                <v-btn
                    v-if="!!user"
                    @click="onSignOut"    
                >
                    Sign Out
                </v-btn>
            </v-row>
        </v-col>
    </v-row>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
    name: "AppBar",
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
        onSignOut() {

        }
    },
    computed: {
        ...mapGetters({
            user: 'user/user'
        })
    }
}
</script>