const deserializeVideoData = (videos) => {
  videos = videos.map((video) => {
    if (video.videoData) {
      video.videoData = JSON.parse(video.videoData)
    }
    if (video.altThumbnails) {
      video.altThumbnails = JSON.parse(video.altThumbnails)
    }
    
    return video
  })

  return videos
}

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
        `videos/all?username=${rootState.users.rootUser.username}`
      );
      
      response.data = deserializeVideoData(response.data)

      commit("videosSet", response.data);
    } catch (exception) {
      return null;
    }
  },
  async videosGetByUsername({ commit, rootState }, params) {
    try {
      const { username } = params;
      const response = await this.$axios.get(`videos/all?username=${username}`);
      response.data = deserializeVideoData(response.data)
      return response.data;
    } catch (exception) {
      return null;
    }
  },
  async videoGet({ commit, rootState }, params) {
    try {
      const response = await this.$axios.get("videos", { params: params });

      if (!response || !response.data) {
        return null;
      }

      response.data = deserializeVideoData([response.data])[0]

      return response.data;
    } catch (exception) {
      return null;
    }
  },
  async getAllVideos({ commit, rootState }) {
    try {
      const response = await this.$axios.get("videos/all");
      response.data = response.data.filter(function (obj) {
        return obj.pk !== "ID#" + rootState.users.rootUser.username;
      });

      response.data = deserializeVideoData(response.data)

      commit("videosSet", response.data);
    } catch (exception) {
      return null;
    }
  },
  async videosPost({}, params) {
    try {
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

  videoUpdate(state, video) {
    if (!video.pk & !video.sk) {
      console.error('Error on store videos/videoUpdate\n\tpk and sk required in params')
    }

    if (!state.videos) {
      state.videos = [video]
      return
    }

    const idx = state.videos.findIndex((vid) => vid.pk == video.pk && vid.sk == vid.sk)

    if (idx == -1) return

    Object.assign(state.videos[idx], video);
  },
};
