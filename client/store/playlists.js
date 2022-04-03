export const state = () => ({
  playlists: null,
  selected_playlist: null,
});

export const getters = {
  playlists: (state) => state.playlists,
  selected_playlist: (state) => state.selected_playlist,
  get_playlist_by_id: (state) => (sk) => {
    return state.playlists.find((playlist) => playlist.sk == sk);
  },
};

export const actions = {
  async playlistsGet({ commit, rootState }) {
    try {
      const response = await this.$axios.get(
        `playlists/all?username=${rootState.user.user.username}`
      );
      commit("playlistsSet", response.data.Items);
    } catch (exception) {
      return null;
    }
  },
  async playlistsGetByUsername({ commit, rootState }, params) {
    try {
      const { username } = params;
      const response = await this.$axios.get(
        `playlists/all?username=${username}`
      );
      return response.data.Items;
    } catch (exception) {
      return null;
    }
  },
  async playlistsGetByVideo({ commit, rootState }, params) {
    try {
      const { username, video } = params;
      const response = await this.$axios.get(
        `playlists/all?username=${username}&video=${video}`
      );
      return response.data.Items;
    } catch (exception) {
      return null;
    }
  },
  async playlistGet({ commit, rootState }, params) {
    try {
      const response = await this.$axios.get("playlists", { params: params });

      if (!response || !response.data || !response.data.Items) {
        return null;
      }

      return response.data.Items[0];
    } catch (exception) {
      return null;
    }
  },
  async getAllplaylists({ commit, rootState }) {
    try {
      const response = await this.$axios.get("playlists/all");

      response.data.Items = response.data.Items.filter(function (obj) {
        return obj.pk !== "ID#" + rootState.user.user.username;
      });

      commit("playlistsSet", response.data.Items);
    } catch (exception) {
      return null;
    }
  },
  async playlistsPost({}, params) {
    try {
      console.log("playlistpost", params);
      const response = await this.$axios.post("playlists", {
        ...params,
      });
      console.log("The post response is:");
      console.log(response);
      return response.data;
    } catch (exception) {
      console.log(exception);
      return null;
    }
  },
  async playlistsPut({}, params) {
    try {
      const response = await this.$axios.put("playlists", params);
      return response.data;
    } catch (exception) {
      return null;
    }
  },
  async playlistsDelete({}, params) {
    try {
      const response = await this.$axios.delete("playlists", { data: params });
      return response.data;
    } catch (exception) {
      return null;
    }
  },
};

export const mutations = {
  playlistsSet(state, array) {
    state.playlists = array;
  },

  playlistUpdate(state, params) {
    if (params.idx == null) {
      console.error("playlistUpdate requires idx in the parameter");
    }

    const idx = params.idx;

    delete params["idx"];

    Object.assign(state.playlists[idx], params);
  },
};
