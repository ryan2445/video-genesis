export const state = () => ({
    rootUser: null,
    users: null,
    otherUserProfile: null
})
export const getters = {
    selected_UserProfile: state => state.otherUserProfile,
    rootUser: state => state.rootUser,
    users: state => state.users
}
export const actions = {
    async userGet({ commit, rootState }) {
        try {
            const response = await this.$axios.get(
                `users/all?username=${rootState.user.user.username}`
            )

            const user = response.data.Items[0]

            commit("rootUserSet", user)

            return user
        } catch (exception) {
            return null
        }
    },
    async usersGet({ commit, rootState }) {
        try {
            const response = await this.$axios.get(
                `users/?username=${rootState.user.user.username}`
            )

            commit("setOtherUserProfile", response.data.Items)
        } catch (exception) {
            return null
        }
    },
    async userPut({ commit, rootState }, params) {
        try {
            const response = await this.$axios.put("users", {
                ...params,
                pk: `ID#${rootState.user.user.username}`,
                sk: "USER"
            })
            return response.data
        } catch (exception) {
            return null
        }
    },
    async userGetByUsername({ commit, rootState }, params) {
        try {
            const { username } = params
            const response = await this.$axios.get(`users/all?username=${username}`)

            return response.data.Items[0]
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
    },
    usersSet(state, users) {
        state.users = users
    }
}
