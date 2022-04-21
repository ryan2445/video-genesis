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
import Banner from "../components/LandingPage/Banner.vue";
import Team from "../components/LandingPage/Team.vue";
import ProjectDemo from "../components/LandingPage/ProjectDemo.vue";
import AppFeatures from "../components/LandingPage/AppFeatures.vue";
import Resources from "../components/LandingPage/Resources.vue";
import Footer from "../components/LandingPage/Footer.vue";
import { mapGetters } from "vuex";

export default {
  components: {
    Banner,
    Team,
    ProjectDemo,
    AppFeatures,
    Resources,
    Footer,
  },
  computed: {
    ...mapGetters({
      user: "users/rootUser",
    }),
  },
  name: "landingpage",
  data() {
    return {};
  },
};
</script>

<style scoped></style>
