export const state = () => ({
    rootUser: null,
    selectedUser: null
})
export const getters = {
    rootUser: state => state.rootUser,
    selectedUser: state => state.selectedUser
}
export const actions = {
    async userGet({ commit, rootState }) {
        try {
            const response = await this.$axios.get('users/auth')
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
    selectedUserSet(state, user) {
        state.selectedUser = user
    }
}
