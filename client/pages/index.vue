

<template>
  <v-main class="pt-0 pt-md-0 px-0 mx-0">
    <!-- This section calls the image link, shows it with text in the center of the image!  -->
    <section>
      <v-parallax src="https://c.pxhere.com/images/9f/8c/70811bfcf51032b0c666b4961e3c-1633063.jpg!d" alt="video-genesis-background">
        <v-layout column align-center justify-center class="white--text">
          <h1
            class="text-xs-center orange--text mb-2 display-1"
            style="font-weight: 1000; text-shadow: 3px 2px #000000"
          >
            Video Genesis
          </h1>
          <div
            class="orange--text subheading mb-3 text-xs-center"
            style="font-weight: 900; text-shadow: 2px 2px #000000"
          >
            super-resolution videos for everyone
          </div>
        </v-layout>
      </v-parallax>
    </section>

    <!-- About Section -->
    <section>
      <v-layout column wrap class="bg-gray-100" align-center>
        <div class="flex flex-row gap-x-4 my-6">
          <v-card 
            v-for="(card, i) of aboutSectionCards"
            :key="`card-${i}`"
            class="flex gap-x-3" style="width: 340px;">
            <v-card-title>
              <h1 class="text-4xl orange--text">
                {{ card.title }}
              </h1>
            </v-card-title>
            <v-divider class="mr-3"></v-divider>
            <v-card-text>
              {{ card.text }}
            </v-card-text>
          </v-card>
        </div>
      </v-layout>
    </section>

    <section>
      <div style="background-color: #ff9800">
        <div>

        </div>
      </div>
    </section>
  </v-main>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters({
      user: "users/rootUser",
    }),
  },
  name: "landingpage",
  data() {
    return {
      team: [
        {
          name: "Mark Minkoff",
          role: "Web developer",
          avatar: "",
        },
        {
          name: "Ryan Hoffman",
          role: "Web developer",
          avatar: "",
        },
        {
          name: "Ritik Bhardwaj",
          role: "Web developer",
          avatar: "",
        },
        {
          name: "Heriberto Martinez",
          role: "Web developer",
          avatar: "",
        },
        {
          name: "Manoj Selvakumar",
          role: "Web developer",
          avatar: "",
        },
      ],
      aboutSectionCards: [
        {
          title: 'About',
          text: 'Video Genesis is a video streaming platform that demonstrates  super-resolution. Users can upscale their videos from low to high resolution.'
        },
        {
          title: 'How it works',
          text: 'Uploaded videos can be processed through a machine learning model called a Super Resolution Generative Adversarial Network (SRGAN). The model is trained by predicting high-resolution images from their low-resolution counterparts.'
        },
        {
          title: 'Features',
          text: "Users can upload videos, stream their own or other's content, create playlists, process videos with super-resolution, interact with videos, and more!"
        }
      ]
    };
  },
};
</script>

<style scoped></style>
