<template>
    <v-app-bar app clipped-left color="orange" elevation="1" style="z-index: 50 !important;">
        <div class="d-flex align-center">
            <NuxtLink to="/" class="mr-4">
                <img src="https://upload.wikimedia.org/wikipedia/commons/1/1a/V_logo.png"
                    class="rounded-full object-cover" style="width:45px; height:45px;" />
            </NuxtLink>
            <div class="text-white font-weight-bold">
                Video Genesis - {{ title }}
            </div>
        </div>
        <v-spacer />
        <div class="mx-6">
            <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                    <v-icon v-bind="attrs" v-on="on">
                        {{ srRunning ? 'icon-wifi-check' : 'icon-wifi-cancel'}}
                    </v-icon>
                </template>
                <span>
                    Super Resolution server is {{ srRunning ? '' : 'not'}} running!
                </span>
            </v-tooltip>
        </div>
        <v-menu offset-y min-width="200px">
            <template v-slot:activator="{ on, attrs }">
                <v-btn v-bind="attrs" v-on="on" fab depressed color="grey lighten-1"
                    width="45" height="45">
                    <img v-if="userProfilePic" style="height:45px; width:45px;"
                        class="rounded-full object-cover" :src="userProfilePic" />
                    <v-icon v-else> mdi-account </v-icon>
                </v-btn>
            </template>
            <v-list>
                <v-list-item-group color="orange">
                    <v-list-item v-for="(item, i) in topBarItems" :key="i"
                        @click="handleClick(item)">
                        <v-list-item-icon class="listItemIcon">
                            <v-icon>{{ item.icon }}</v-icon>
                        </v-list-item-icon>
                        <v-list-item-content>
                            <v-list-item-title>
                                {{ item.title }}
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-menu>
    </v-app-bar>
</template>
<script>
import { mapGetters } from 'vuex'
export default {
    data() {
        return {
            topBarItems: [
                {
                    title: 'Account Settings',
                    color: 'orange',
                    icon: 'mdi-account',
                    route: '/account'
                },
                {
                    title: 'Sign Out',
                    icon: 'mdi-logout-variant',
                    method: 'signOut'
                }
            ]
        }
    },
    methods: {
        handleClick(item) {
            if (item.route) return this.$router.push(item.route)

            if (item.method) return this[item.method]()
        },
        async signOut() {
            await this.$auth.signOut()
            this.$store.commit('users/rootUserSet', null)
            this.$store.commit('auth/clearToken')
            this.$router.push('/')
        }
    },
    computed: {
        title() {
            return this.$store.getters['app/route']
        },
        ...mapGetters({
            user: 'users/rootUser',
            srRunning: 'sr/running'
        }),
        userProfilePic() {
            // If the user does not exist, return null
            if (!this.user) return null

            return this.user.profilePicKey
        }
    }
}
</script>
<style scoped>
.v-application--is-ltr .v-list-item__action:first-child,
.v-application--is-ltr .v-list-item__icon:first-child {
    margin-right: 16px;
}
</style>
