const BASE_URI = 'https://n1ddeh.ngrok.io'

export const state = () => ({
  running: false,
});

export const getters = {
  running: (state) => state.running,
};

export const mutations = {
  runningSet: (state, bool) => {
    state.running = bool
  }
};

export const actions = {
  async checkServer({commit}) {
    try {
      const resp = await this.$axios.get(BASE_URI)
      commit('runningSet', true)
    }
    catch(e) {
      console.log('Super Resolution server is not running\n', e)
    }
  },
  async processVideo(_, { video_url, video_key }) {
    try {
      const URL = BASE_URI + '/process'
      const payload = { video_url, video_key }
      const resp = await this.$axios.post(URL, payload)
    }
    catch(e) {
      console.error('Error in processing video for SR\n', e)
    }
  }
}
