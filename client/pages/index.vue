<template>
  <v-main>
    <div class="bg-color-image">
      <div class="bg-image">
        <Banner />
        <Team />
        <ProjectDemo />
        <AppFeatures />
        <Resources />
        <Footer />
      </div>
    </div>
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
import Dashboard from "../layouts/dashboard.vue";

export default {
  components: {
    Banner,
    Team,
    ProjectDemo,
    AppFeatures,
    Resources,
    Footer,
    Dashboard,
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

<style scoped>
.bg-color-image {
  background: #2e1226;
}
.bg-image {
  background: no-repeat url(@/assets/images/banner-img.png);
  background-size: contain;
}
</style>
