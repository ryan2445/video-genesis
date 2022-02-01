<template>
    <v-app-bar app flat color="white">
        <v-spacer />
        <v-menu offset-y min-width="200px">
            <template v-slot:activator="{ on, attrs }">
                <v-btn v-bind="attrs" v-on="on" icon color="grey darken-1">
                    <v-icon>
                        mdi-account
                    </v-icon>
                </v-btn>
            </template>
            <v-list>
                <v-list-item-group color="orange">
                    <v-list-item v-for="(item, i) in topBarItems" :key="i"
                        :to="item.route">
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
                    icon: 'mdi-emoticon-cool-outline',
                    route: '/account'
                }
            ]
        }
    },
    computed: {
        ...mapGetters({
            user: 'user/user'
        })
    }
}
</script>
<style scoped>
.v-application--is-ltr .v-list-item__action:first-child,
.v-application--is-ltr .v-list-item__icon:first-child {
    margin-right: 16px;
}
</style>
