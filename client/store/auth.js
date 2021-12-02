// import { fromCognitoIdentityPool as FromCognitoIdentityPool } from "@aws-sdk/credential-provider-cognito-identity"
// import { CognitoIdentityClient } from "@aws-sdk/client-cognito-identity"
// import { idToken } from "./misc"

// const identityPoolId = 'us-west-2:a7e3dcf8-8ead-4d2f-b0c5-c9b2fca24109'
// const identityProvider = import.meta.env.VITE_APP_COGNITO_IDENTITY_PROVIDER
// const region = 'us-west-2'

export const state = () => ({
    token: null
})

export const getters = {
    token: (state) => state.token
}

export const mutations = {
    setToken(state, token) {
        state.token = token
    }
}

export const actions = {
    async authorize({commit}, {auth, axios}) {
        // Get the JWT token
        const jwtToken = (await auth.currentSession()).getAccessToken().getJwtToken()

        // Set the token here
        commit('setToken', jwtToken)

        // Set the authorization header token
        axios.defaults.headers.common['Authorization'] = jwtToken
    },
    async unauthorize({commit}, {axios}) {
        // Set the current token to null
        commit('setToken', null)

        // Unset the auth header
        axios.defaults.headers.common['Authorization'] = null
    }
}
