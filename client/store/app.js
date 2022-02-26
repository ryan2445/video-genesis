// import { fromCognitoIdentityPool as FromCognitoIdentityPool } from "@aws-sdk/credential-provider-cognito-identity"
// import { CognitoIdentityClient } from "@aws-sdk/client-cognito-identity"
// import { idToken } from "./misc"

// const identityPoolId = 'us-west-2:a7e3dcf8-8ead-4d2f-b0c5-c9b2fca24109'
// const identityProvider = import.meta.env.VITE_APP_COGNITO_IDENTITY_PROVIDER
// const region = 'us-west-2'

export const state = () => ({
  route: "Home"
})

export const getters = {
  route: (state) => {
    return state.route.replace(/(\w)(\w*)/g, function(g0,g1,g2){return g1.toUpperCase() + g2.toLowerCase();});
  }
}

export const mutations = {
  setRoute(state, route) {
      state.route = route
  }
}

export const actions = {

}
