export default {
  // Disable server-side rendering: https://go.nuxtjs.dev/ssr-mode
  ssr: false,

  // Target: https://go.nuxtjs.dev/config-target
  target: "static",

  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: "video-genesis",
    htmlAttrs: {
      lang: "en",
    },
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "" },
      { name: "format-detection", content: "telephone=no" },
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [
    "@/assets/icons/icons.css",
    "node_modules/videojs-resolution-switcher-webpack/lib/videojs-resolution-switcher.css",
    "video.js/dist/video-js.min.css",
  ],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: "~/plugins/amplify.js" },
    { src: "~/plugins/vee-validate.js" },
    { src: "~/plugins/axios.js" },
    { src: "~/plugins/s3-client.js" },
    { src: "~/plugins/tensor.js" },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: ["@nuxtjs/tailwindcss", "@nuxtjs/pwa"],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [["@nuxtjs/vuetify", { defaultAssets: { icons: "mdi" } }]],

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    transpile: ["vee-validate/dist/rules"],
  },

  router: {
    middleware: ["authMiddleware"],
  },

  //    Vuetify config
  vuetify: {
    theme: {
      themes: {
        light: {
          anchor: "#ffa726",
        },
      },
    },
  },
};
