export const state = () => ({
  user: null,
  otherUserProfile: null,
});

export const getters = {
  selected_UserProfile: (state) => state.otherUserProfile,
  rootUser: (state) => state.user,
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
  async usersGet({ commit, rootState }) {
    try {
      const response = await this.$axios.get(
        `users/?username=${rootState.user.user.username}`
      );

      commit("setOtherUserProfile", response.data.Items);
    } catch (exception) {
      return null;
    }
  },

  async userPut({ commit, rootState }, params) {
    try {
      const response = await this.$axios.put("users", {
        ...params,
        pk: `ID#${rootState.user.user.username}`,
        sk: "USER",
      });
      console.log(response.data);
      return response.data;
    } catch (exception) {
      return null;
    }
  },
  async userGetByUsername({commit, rootState}, params)
  {
    try {
      const {username} = params; 
      const response = await this.$axios.get(
        `users/all?username=${username}`
      );
      return response.data.Items; 

    } catch (exception) {
      return null;
    }

  }
};

export const mutations = {
  userSet(state, array) {
    state.user = array;
  },

  otherUserProfileSet(state, array) {
    state.otherUserProfile = array;
  },
};
