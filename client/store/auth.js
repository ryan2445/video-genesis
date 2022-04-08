import axios from "axios";
import { S3Client } from "@aws-sdk/client-s3"
const { fromCognitoIdentityPool } = require("@aws-sdk/credential-providers")
const REGION = "us-west-2"
export const state = () => ({
	s3: null
})
export const getters = {
	token: state => state.token,
	s3: state => state.s3,
}
export const mutations = {
	clearToken() {
		localStorage.idToken = null
		localStorage.accessToken = null
		axios.defaults.headers.common['Authorization'] = null
	},
	setToken(_, session) {
		const accessToken = session.accessToken.jwtToken

		const idToken = session.idToken.jwtToken

		localStorage.idToken = idToken

		localStorage.accessToken = accessToken

		axios.defaults.headers.common["Authorization"] = `Bearer ${idToken}`
	},
	setS3: (state, s3) => state.s3 = s3
}
export const actions = {
	async inits3({commit}) {
		try {
			const token = localStorage.idToken
		
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
