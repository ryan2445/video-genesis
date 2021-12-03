export default async function ({ app, route, store, redirect }) {
    //  Ignore auth middleware on home, signin, and signup routes
    if (route.path == '/' || route.path == '/auth/sign-in' || route.path == '/auth/sign-up') return

    //  Check if there's a logged in user
    const user = await app.$auth.currentAuthenticatedUser()

    //  If not, redirec to signin
    if (!user) return redirect('/auth/sign-in')

    //  If there is a logged in user, set the user in the store
    return store.commit('user/setUser', user)
}
