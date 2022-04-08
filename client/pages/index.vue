<!-- This section calls the image link, shows it with text in the center of the image!  -->

<template>
    <v-main class="pt-0 pt-md-0 px-0 mx-0">
        <section>
            <v-parallax :src="imageLink.img">
                <v-layout column align-center justify-center class="white--text">
                    <h1 class="text-xs-center orange--text mb-2 display-1"
                        style="font-weight: 1000; text-shadow: 3px 2px #000000">
                        Stream videos With High Resolution
                    </h1>
                    <div class="orange--text subheading mb-3 text-xs-center"
                        style="font-weight: 900; text-shadow: 2px 2px #000000">
                        Even if you are experiencing low bandwidth
                    </div>
                </v-layout>
            </v-parallax>
        </section>
        <!-- This section creates our v-card containers/components which we are using to show our users what this web application is about!  -->
        <section>
            <v-layout column wrap class="my-5" align-center>
                <v-flex xs12>
                    <v-container grid-list-xl>
                        <v-layout row wrap align-center>
                            <v-flex xs12 md4>
                                <v-card class="elevation-0 transparent">
                                    <v-card-text class="text-xs-center">
                                        <v-icon x-large
                                            class="orange--text text--lighten-2">About
                                        </v-icon>
                                    </v-card-text>
                                    <v-card-text>
                                        Video Genesis, a video streaming platform will
                                        allow the
                                        users with low bandwidth access to stream videos
                                        with high
                                        resolution. By using this web application, users
                                        will be
                                        able to upload videos and stream videos in high
                                        quality
                                        resolutions.
                                    </v-card-text>
                                </v-card>
                            </v-flex>
                            <v-flex xs12 md4>
                                <v-card class="elevation-0 transparent">
                                    <v-card-text class="text-xs-center">
                                        <v-icon x-large
                                            class="orange--text text--lighten-2">How it
                                            works</v-icon>
                                    </v-card-text>
                                    <v-card-text>
                                        This application utilizes a machine learning model
                                        which
                                        uses super-resolution imaging to increase the
                                        quality of
                                        low-resolution video when network speeds are
                                        limited. The
                                        videos uploaded by the users will train the
                                        machine learning
                                        model and will improve the quality of the video
                                        over time.
                                    </v-card-text>
                                </v-card>
                            </v-flex>
                            <v-flex xs12 md4>
                                <v-card class="elevation-0 transparent">
                                    <v-card-text class="text-xs-center">
                                        <v-icon x-large
                                            class="orange--text text--lighten-2">Features
                                        </v-icon>
                                    </v-card-text>
                                    <v-card-text>
                                        Video Genesis will allow users to create their own
                                        account
                                        and users will be able to upload the video to
                                        their account
                                        and stream the video in high resolution! Users
                                        will have an
                                        option to edit or delete their metadata and also
                                        have access
                                        to watch other users videos.
                                    </v-card-text>
                                </v-card>
                            </v-flex>
                        </v-layout>
                    </v-container>
                </v-flex>
            </v-layout>
        </section>

        <!-- This piece of code creates a container in orange color and than by using v-card, we show names of our team members and their role-->

        <section>
            <!-- <v-container class="orange"> -->
            <div style="background-color: #ff9800">
                <v-row>
                    <v-col lg="8">
                        <v-icon x-large class="black--text text--lighten-2">Team</v-icon>
                    </v-col>
                </v-row>
                <center>
                    <v-layout row wrap justify-center>
                        <v-flex xs12 sm6 md4 lg3 v-for="member in team"
                            :key="member.name">
                            <v-card flat class="orange text-xs-center ma-9">
                                <v-responsive class="pt-2" justify-center>
                                    <v-avatar size="150" class="grey lighten-2 center">
                                        <img :src="member.avatar" />
                                    </v-avatar>
                                </v-responsive>

                                <v-card-text>
                                    <div class="subheading mb-1 text-xs-center">
                                        {{ member.name }}
                                    </div>
                                    <div class="grey--text mb-2 justify-center">
                                        {{ member.role }}
                                    </div>
                                </v-card-text>
                            </v-card>
                        </v-flex>
                    </v-layout>
                </center>
            </div>
        </section>
        <!-- This section creates a footer with text to show! -->
        <v-footer class="blue">
            <div class="black--text">
                Copyright 2021 Genesis LLC. All Rights Reserved
            </div>
        </v-footer>
    </v-main>
</template>

<script>
import { mapGetters } from 'vuex'
import AuthForm from '../components/AuthForm.vue'

export default {
    components: { AuthForm },
    computed: {
        ...mapGetters({
            user: 'users/rootUser'
        })
    },
    name: 'landingpage',
    data: function () {
        return {
            team: [
                {
                    name: 'Mark Minkoff',
                    role: 'Web developer',
                    avatar: 'https://static0.gamerantimages.com/wordpress/wp-content/uploads/2021/10/marvels-avengers-3.jpg'
                },

                {
                    name: 'Ryan Hoffman',
                    role: 'Web developer',
                    avatar: 'https://i2.wp.com/www.comicsbeat.com/wp-content/uploads/2021/09/Eh-Steve.jpg?fit=1200%2C630&ssl=1'
                },

                {
                    name: 'Ritik Bhardwaj',
                    role: 'Web developer',
                    avatar: 'https://cdnb.artstation.com/p/assets/images/images/027/360/123/large/andrey-spiridonov-cosplay-aniventure-2018-27-thor-avengers-infinity-war-asp-0972p.jpg?1591301884'
                },
                {
                    name: 'Heriberto Martinez',
                    role: 'Web developer',
                    avatar: 'https://m.media-amazon.com/images/I/71A+RlBsJRL._AC_SX569_.jpg'
                },

                {
                    name: 'Manoj Selvakumar',
                    role: 'Web developer',
                    avatar: 'https://cdn.vox-cdn.com/thumbor/K5IUSjv1ArPfjh_IZUp4DPsoZMY=/1400x1400/filters:format(png)/cdn.vox-cdn.com/uploads/chorus_asset/file/22024938/marvels_spiderman_remastered_screenshot_01_disclaimer_en_01oct20.png'
                }
            ],
            imageLink: {
                img: 'https://cdn.pixabay.com/photo/2018/02/28/10/04/soap-bubble-3187617_1280.jpg'
            }
        }
    }
}
</script>

<style scoped></style>
