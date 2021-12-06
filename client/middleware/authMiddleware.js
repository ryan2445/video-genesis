export default async function ({ $axios, $auth, route, store, redirect }) {
	//  Ignore auth middleware on home, signin, and signup routes
	if (
		route.path == '/' ||
		route.path == '/auth/sign-in' ||
		route.path == '/auth/sign-up'
	)
		return

	//  Get the cognito user's idtoken
	const session = await $auth.currentSession()

	//  If not logged in, redirect to signin
	if (!session) return redirect('/auth/sign-in')

	//  Get the identity of the user
	const identity = session.getIdToken()

	//  Get the user's JWT
	const token = identity.getJwtToken()

	//  Set the Authorization token for all axios requests
	$axios.defaults.headers.common['Authorization'] = token

	//  If there is a logged in user, set the user in the store
	return store.commit('user/setUser', {
		username: identity.payload['cognito:username']
	})
}
