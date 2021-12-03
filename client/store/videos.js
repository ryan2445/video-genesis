export const state = () => ({
    videos: null
})

export const getters = {
    videos: (state) => state.videos
}

export const actions = {
    async videosGet({commit, rootState}) {
        const response = await this.$axios.get(`videos?username=${rootState.user.user.username}`)

        commit('videosSet', response.data.Items)
    }
}

export const mutations = {
    videosSet(state, array) {
        state.videos = array
    }
}
