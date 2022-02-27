export const state = () => ({
	route: "Home"
})

export const getters = {
	route: state => {
		return state.route.replace(/(\w)(\w*)/g, function (g0, g1, g2) {
			return g1.toUpperCase() + g2.toLowerCase()
		})
	}
}

export const mutations = {
	setRoute(state, route) {
		state.route = route
	}
}

export const actions = {}
