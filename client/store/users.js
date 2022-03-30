export const state = () => ({
    rootUser: null,
    otherUserProfile: null
})
export const getters = {
    selected_UserProfile: state => state.otherUserProfile,
    rootUser: state => state.rootUser
}
export const actions = {
    async userGet({ commit, rootState }) {
        try {
            const response = await this.$axios.get(
                `users/all?username=${rootState.user.user.username}`
            )
            const user = response.data
            commit("rootUserSet", user)
            return user
        } catch (exception) {
            return null
        }
    },
    async userPut({}, params) {
        try {
            const response = await this.$axios.put("users", params)
            return response.data
        } catch (exception) {
            return null
        }
    },
    async userGetByUsername({}, username) {
        try {
            const response = await this.$axios.get(`users/all?username=${username}`)
            return response.data
        } catch (exception) {
            return null
        }
    },
    async usersGetVotes({}, params) {
        try {
            const response = await this.$axios.get(
                `users/votes?videoId=${params.videoId}`
            )
            return response.data
        } catch (exception) {
            return null
        }
    },
    async usersPostVotes({}, params) {
        try {
            const response = await this.$axios.post("/users/votes", params)
            return response.data
        } catch (exception) {
            return null
        }
    }
}
export const mutations = {
    rootUserSet(state, user) {
        state.rootUser = user
    },
    otherUserProfileSet(state, array) {
        state.otherUserProfile = array
    }
}
