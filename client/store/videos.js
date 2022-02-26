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
  videosAll: (state) => state.videosAll
};

export const actions = {
  async videosGet({ commit, rootState }) {
    try {
      const response = await this.$axios.get(
        `videos/all?username=${rootState.user.user.username}`
      );
      commit("videosSet", response.data.Items);
    } catch (exception) {
      return null;
    }
  },
  async videoGet({ commit, rootState }, params) {
    try {
      const response = await this.$axios.get('videos', { params: params });

      if (!response || !response.data || !response.data.Items) {
        return null;
      }

      return response.data.Items[0]
    }
    catch (exception) {
      return null;
    }
  },
  async getAllVideos({ commit, rootState }) {
    try {
      const response = await this.$axios.get("videos/all");
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
      const response = await this.$axios.delete("videos", { data: params });
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

  videosSetAll(state, array) {
    state.videosAll = array;
  },

  videoUpdate(state, params) {
    if (params.idx == null) {
      console.error("videoUpdate requires idx in the parameter")
    }

    const idx = params.idx

    delete params['idx']
    
    Object.assign(state.videos[idx], params)
  }
};
