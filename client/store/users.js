export const state = () => ({
  user: null,
  otherUserProfile: null,
});

export const getters = {
  selected_UserProfile: (state) => state.otherUserProfile,
  get_user_by_id: (state) => (sk) => {
    return state.videos.find((user) => user.sk == sk);
  },
};

export const actions = {
  async userGet({ commit, rootState }) {
    try {
      const response = await this.$axios.get(
        `users/all?username=${rootState.user.user.username}`
      );
      commit("userSet", response.data.Items);
    } catch (exception) {
      return null;
    }
  },
  async usersGet({ commit, rootState }, params) {
    try {
      const response = await this.$axios.get(`users/all?username=${params}`);

      commit("setOtherUserProfile", response.data.Items);
    } catch (exception) {
      return null;
    }
  },

  async userPut({ commit, rootState }, params) {
    try {
      const response = await this.$axios.post("users", {
        ...params,
        username: rootState.user.user.username,
      });
      return response.data;
    } catch (exception) {
      return null;
    }
  },
};

export const mutations = {
  userSet(state, array) {
    state.user = array;
  },

  otherUserProfileSet(state, array) {
    state.otherUserProfile = array;
  },
};
