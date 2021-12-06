<template>
    <v-app light>
    <v-content>
      <section>
        <v-parallax :src="imageLink.sub_main" height="600">
          <v-layout column align-center justify-center class="white--text">
            <h1 class=" text-xs-center orange--text mb-2 display-1" style="font-weight: 1000; text-shadow: 3px 2px #000000">Stream videos With High Resolution</h1>
            <div class="orange--text subheading mb-3 text-xs-center" style="font-weight: 900; text-shadow: 2px 2px #000000">Even if you are experiencing low bandwidth</div>
          </v-layout>
        </v-parallax>
      </section>

      <section>
        <v-layout
          column
          wrap
          class="my-5"
          align-center
        >
          <v-flex xs12>
            <v-container grid-list-xl>
              <v-layout row wrap align-center>
                <v-flex xs12 md4>
                  <v-card class="elevation-0 transparent">
                    <v-card-text class="text-xs-center">
                      <v-icon x-large class="orange--text text--lighten-2">About</v-icon>
                    </v-card-text>
                    <v-card-text>
                      Video Genesis, a video streaming platform will allow the users with low bandwidth access to stream videos with high resolution. By using this web application, users will be able to upload videos and stream videos in high quality resolutions.
                    </v-card-text>
                  </v-card>
                </v-flex>
                <v-flex xs12 md4>
                  <v-card class="elevation-0 transparent">
                    <v-card-text class="text-xs-center">
                      <v-icon x-large class="orange--text text--lighten-2">How it works</v-icon>
                    </v-card-text>
                    <v-card-text>
                      This application utilizes a machine learning model which uses super-resolution imaging to increase the quality of low-resolution video when network speeds are limited. The videos uploaded by the users will train the machine learning model and will improve the quality of the video over time.
                    </v-card-text>
                  </v-card>
                </v-flex>
                <v-flex xs12 md4>
                  <v-card class="elevation-0 transparent">
                    <v-card-text class="text-xs-center">
                      <v-icon x-large class="orange--text text--lighten-2">Features</v-icon>
                    </v-card-text>
                    <v-card-text>
                      Video Genesis will allow users to create their own account and users will be able to upload the video to their account and stream the video in high resolution!
                    </v-card-text>
                  </v-card>
                </v-flex>
              </v-layout>
            </v-container>
          </v-flex>
        </v-layout>
      </section>

      
    

       <section>
        <v-container class="orange">
            <v-row>
        <v-col lg="10">
            <v-icon x-large class="black--text text--lighten-2">Team</v-icon>
        </v-col>
      </v-row>
           
           <v-layout row wrap>
        <v-flex xs12 sm6 md4 lg3 v-for="person in team" :key="person.name">
          <v-card flat class="orange text-xs-center ma-3">
             
            <v-responsive class="pt-4">
              <v-avatar size="150" class="grey lighten-2">
               
              </v-avatar>
            </v-responsive>
            <v-card-text>
              <div class="subheading">{{ person.name }}</div>
              <div class="grey--text">{{ person.role }}</div>
            </v-card-text>
            <v-card-actions>
             
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
        </v-container>
     </section>

      <v-footer class="blue darken-2">
        <v-layout row wrap align-center>
          <v-flex xs12 class="text-xs-center">
            <div class="white--text ml-3">
              Copyright 2021 Genesis LLC. All Rights Reserved
            </div>
          </v-flex>
        </v-layout>
      </v-footer>

    </v-content>
</v-app>
</template>

<script>
import { mapGetters } from 'vuex'
import AuthForm from '../components/AuthForm.vue'

export default {
    components: { AuthForm },
    computed: {
        ...mapGetters({
            user: 'user/user'
        })
    },
  name: "App",
  data: function() {
    return {
      imageLink: {
        sub_main:
          "https://cdn.pixabay.com/photo/2018/02/28/10/04/soap-bubble-3187617_1280.jpg",
        
      },
      team: [
        { name: 'Mark Minkoff', role: 'Web developer', avatar: 'https://news.mit.edu/sites/default/files/styles/news_article__image_gallery/public/images/202012/MIT-Coding-Brain-01-press_0.jpg?itok=JKoUflf8' },
        { name: 'Ryan Hoofman', role: 'Web developer', avatar: '/avatar-2.png' },
        { name: 'Ritik Bhardwaj', role: 'Web developer', avatar: '/avatar-3.png' },
        { name: 'Heriberto Martinez', role: 'Web developer', avatar: '/avatar-4.png' },
        { name: 'Manoj Selvakumar', role: 'Web developer', avatar: '/avatar-5.png'}
      ]
      }    
          }
  }
      
</script>

<style scoped>
.finedTitle {
  font-weight: 900;
  text-shadow: 2px 2px #000000;
}

.social-icon {
  font-size: 21px;
  color: white;
}
</style>

