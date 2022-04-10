export default async function ({ $axios, route, store, redirect }) {
  //  Set ignore routes
  const ignore = ["/", "/auth/sign-in", "/auth/sign-up", "/auth/confirm", "/auth/reset"]

  //  If path is in ignore list, continue
  if (ignore.includes(route.path)) return

  //  Try to get IdToken from localStorage
  const token = localStorage.idToken

  //  If they have a token in local storage, let them continue
  //  Any request they make with an invalid token will boot them back to signin
  if (token) {
    //  Set the Authorization token for all axios requests
    $axios.defaults.headers.common["Authorization"] = token

    //  If the user's profile isn't loaded, fetch their profile
    if (!store.getters['users/rootUser']) await store.dispatch("users/userGet")

    return
  }

  //  If no IdToken set, boot to signin
  return redirect("/auth/sign-in")
}
