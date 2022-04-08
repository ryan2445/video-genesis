module.exports = {
  theme: {
    extend: {
      colors: {
        "app-orange": "#FF7A45",
      },
    },
  },
  variants: {},
  plugins: [require("@tailwindcss/line-clamp")],
  purge: {
    content: [
      `components/**/*.{vue,js}`,
      `layouts/**/*.vue`,
      `pages/**/*.vue`,
      `plugins/**/*.{js,ts}`,
      `nuxt.config.{js,ts}`,
    ],
  },
};
