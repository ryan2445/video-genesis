export const state = () => ({
  videos: null,
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
        `videos/all?username=${rootState.user.user.username}`
      );
      commit("videosSet", response.data.Items);
    } catch (exception) {
      return null;
    }
  },
  async videosGetByUsername({ commit, rootState }, params) {
    try {
      const { username } = params;
      const response = await this.$axios.get(`videos/all?username=${username}`);
      return response.data.Items;
    } catch (exception) {
      return null;
    }
  },
  async videoGet({ commit, rootState }, params) {
    try {
      const response = await this.$axios.get("videos", { params: params });

      if (!response || !response.data || !response.data.Items) {
        return null;
      }

      return response.data.Items[0];
    } catch (exception) {
      return null;
    }
  },
  async getAllVideos({ commit, rootState }) {
    try {
      const response = await this.$axios.get("videos/all");

      response.data.Items = response.data.Items.filter(function (obj) {
        return obj.pk !== "ID#" + rootState.user.user.username;
      });

      commit("videosSet", response.data.Items);
    } catch (exception) {
      return null;
    }
  },
  async videosPost({}, params) {
    try {
      console.log("videopost", params);
      const response = await this.$axios.post("videos", {
        ...params,
      });
      return response.data;
    } catch (exception) {
      return null;
    }
  },
  async videosPut({}, params) {
    try {
      const response = await this.$axios.put("videos", params);
      return response.data;
    } catch (exception) {
      return null;
    }
  },
  async videosDelete({}, params) {
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

  videoUpdate(state, params) {
    if (params.idx == null) {
      console.error("videoUpdate requires idx in the parameter");
    }

    const idx = params.idx;

    delete params["idx"];

    Object.assign(state.videos[idx], params);
  },
};
