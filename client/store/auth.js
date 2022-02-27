import { S3Client } from "@aws-sdk/client-s3"
const { fromCognitoIdentityPool } = require("@aws-sdk/credential-providers")
const REGION = "us-west-2"

export const state = () => ({
	token: null,
	s3: null
})

export const getters = {
	token: state => state.token,
	s3: state => state.s3
}

export const mutations = {
	setToken(state, token) {
		state.token = token
	},
	setS3(state, s3) {
		state.s3 = s3
	}
}

export const actions = {
	async authorize({ commit, dispatch }, { auth, axios }) {
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
	},
	async inits3({commit}, $auth) {
		try {
			const session = await $auth.currentSession()
			const identity = session.getIdToken()
			const token = identity.getJwtToken()
		
			const s3 = new S3Client({
				region: REGION,
				credentials: fromCognitoIdentityPool({
					clientConfig: { region: REGION },
					identityPoolId: "us-west-2:a7e3dcf8-8ead-4d2f-b0c5-c9b2fca24109",
					logins: {
						"cognito-idp.us-west-2.amazonaws.com/us-west-2_3LjdLzhH5": token
					}
				})
			})

			commit('setS3', s3)
		}
		catch(e) {
			console.error("Tried to initialize s3")
			return null
		}
	}
}
