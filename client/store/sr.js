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
      const resp = await this.$axios.get('https://n1ddeh.ngrok.io')
      commit('runningSet', true)
    }
    catch(e) {
      console.log('Super Resolution server is not running')
    }
  }
}
