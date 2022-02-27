export const state = () => ({
	token: null
})

export const getters = {
	token: state => state.token
}

export const mutations = {
	setToken(state, token) {
		state.token = token
	}
}

export const actions = {
	async authorize({ commit }, { auth, axios }) {
		// Get the JWT token
		const jwtToken = (await auth.currentSession())
			.getAccessToken()
			.getJwtToken()

		// Set the token here
		commit("setToken", jwtToken)

		// Set the authorization header token
		axios.defaults.headers.common["Authorization"] = jwtToken
	},
	async unauthorize({ commit }, { axios }) {
		// Set the current token to null
		commit("setToken", null)

		// Unset the auth header
		axios.defaults.headers.common["Authorization"] = null
	}
}
