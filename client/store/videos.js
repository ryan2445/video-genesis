export const state = () => ({
  videos: null,
  videosAll: null,
  selected_video: null,
});

export const getters = {
  videos: (state) => state.videos,
  selected_video: (state) => state.selected_video,
  get_video_by_id: (state) => (sk) => {
    return state.videos.find((video) => video.sk == sk);
  },
};

export const actions = {
  async videosGet({ commit, rootState }) {
    try {
      const response = await this.$axios.get(
        `videos?username=${rootState.user.user.username}`
      );
      commit("videosSet", response.data.Items);
    } catch (exception) {
      return null;
    }
  },
  async GetAllVideos({ commit, rootState }) {
    try {
      const response = await this.$axios.get("videos");
      commit("videosSetAll", response.data.Items);
    } catch (exception) {
      return null;
    }
  },
  async videosPost({ commit, rootState }, params) {
    try {
      const response = await this.$axios.post("videos", {
        ...params,
        username: rootState.user.user.username,
      });
      return response.data;
    } catch (exception) {
      return null;
    }
  },
  async videosPut({ commit, rootState }, params) {
    try {
      const response = await this.$axios.put("videos", params);
      return response.data;
    } catch (exception) {
      return null;
    }
  },
  async videosDelete({ commit, rootState }, params) {
    try {
      const response = await this.$axios.delete("videos", params);
      return response.data;
    } catch (exception) {
      return null;
    }
  },
};

export const mutations = {
  videosSet(state, array) {
    state.videos = array;
  },

  videoSetAll(state, array) {
    state.videosAll = array;
  },
};
