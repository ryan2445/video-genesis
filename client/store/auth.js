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
        const jwtToken = (await auth.currentSession()).getAccessToken().getJwtToken()

        commit('setToken', jwtToken)

        axios.defaults.headers.common['Authorization'] = jwtToken
    }
}
