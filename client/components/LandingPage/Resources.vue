<template>
  <div class="resources">
    <div class="container">
      <div class="mt-24 mb-32">
        <v-row>
          <v-col cols="12" class="white--text">
            <h4 class="text-4xl font-medium">Resources</h4>
            <div class="border-divide-red"></div>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12" class="mt-4 white--text">
            <a href="https://vuejs.org/"
              ><div class="sub-accordions text-white">
                <h4 class="text-3xl font-medium">Vue.js Framework</h4>
                <h6 class="text-lg">
                  A progressive frontend Javascript framework for constructing
                  user interfaces. It is commonly used to build Single-Page
                  Applications. It provides developers with tooling and
                  libraries to create dynamic web applications.
                </h6>
              </div></a
            >

            <div class="border-divide-white"></div>
          </v-col>
          <v-col cols="12" class="mt-4 white--text">
            <a href="https://tailwindcss.com/"
              ><div class="sub-accordions text-white">
                <h4 class="text-3xl font-medium">TailwindCSS</h4>
                <h6 class="text-lg">
                  A progressive frontend Javascript framework for constructing
                  user interfaces. It is commonly used to build Single-Page
                  Applications. It provides developers with tooling and
                  libraries to create dynamic web applications.
                </h6>
              </div>
            </a>

            <div class="border-divide-white"></div>
          </v-col>
          <v-col cols="12" class="mt-4 white--text">
            <a href="https://aws.amazon.com/"
              ><div class="sub-accordions text-white">
                <h4 class="text-3xl font-medium">Amazon Web Services</h4>
                <h6 class="text-lg">
                  An on-demand cloud computing platform that provides numerous
                  cloud computing services like virtual servers and databases.
                </h6>
              </div></a
            >

            <div class="border-divide-white"></div>
          </v-col>
          <v-col cols="12" class="mt-4 white--text">
            <a href="https://www.geeksforgeeks.org/super-resolution-gan-srgan/"
              ><div class="sub-accordions text-white">
                <h4 class="text-3xl font-medium">
                  Super Resolution Generative Adversarial Network
                </h4>
                <h6 class="text-lg">
                  A progressive frontend Javascript framework for constructing
                  user interfaces. It is commonly used to build Single-Page
                  Applications. It provides developers with tooling and
                  libraries to create dynamic web applications.
                </h6>
              </div></a
            >

            <div class="border-divide-white"></div>
          </v-col>
          <v-col cols="12" class="mt-4 white--text">
            <a href="https://videojs.com/"
              ><div class="sub-accordions text-white">
                <h4 class="text-3xl font-medium">VideoJS</h4>
                <h6 class="text-lg">
                  A javascript based framework which uses HTML5 video
                  functionality.
                </h6>
              </div></a
            >

            <div class="border-divide-white"></div>
          </v-col>
        </v-row>
      </div>
    </div>
  </div>
</template>

<style scoped>
.resources {
  background: #240e1e;
}

.sub-accordions:hover {
  color: #ffed85;
}
.container {
  margin: auto;
  width: 90%;
}
.border-divide-red {
  border: 1px solid #a13440;
  margin-top: 1rem;
}
.border-divide-white {
  border: 0.5px solid white;
  margin-top: 1rem;
  opacity: 50%;
}
a,
a:hover,
a:visited,
a:active {
  color: inherit;
  text-decoration: none;
}
</style>
