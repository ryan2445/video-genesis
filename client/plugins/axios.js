import axios from "axios";

const instance = axios.create({
  baseURL:
    "https://zkcsvdswr2.execute-api.us-west-2.amazonaws.com/Prod/" ||
    "http://localhost:3001/", //Prod api url: https://zkcsvdswr2.execute-api.us-west-2.amazonaws.com/Prod/
  timeout: 5000,
  headers: {},
});

// This allows us to access axios in any context by calling this.$axios
export default ({ redirect }, inject) => {
  instance.interceptors.response.use(
    response => response,
    error => {
      const err = error.toJSON()
      const isUnauthorized = err.status == 401 || err.status == 403
      const isUpscaling = err.config.url == 'https://n1ddeh.ngrok.io'
      if(isUnauthorized && !isUpscaling) {
        redirect("/auth/sign-in")
      }
      return Promise.reject(error)
    }
  )

  inject("axios", instance)
}
