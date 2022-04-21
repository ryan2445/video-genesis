<template>
  <v-main>
    <Banner />
    <Team />
    <ProjectDemo />
    <AppFeatures />
    <Resources />
    <Footer />
  </v-main>
</template>

<script>
import Banner from "../components/LandingPage/Banner.vue"
import Team from "../components/LandingPage/Team.vue"
import ProjectDemo from "../components/LandingPage/ProjectDemo.vue"
import AppFeatures from "../components/LandingPage/AppFeatures.vue"
import Resources from "../components/LandingPage/Resources.vue"
import Footer from "../components/LandingPage/Footer.vue"
import { mapGetters } from "vuex";

export default {
  components: {
    Banner,
    Team,
    ProjectDemo,
    AppFeatures,
    Resources,
    Footer
  },
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
