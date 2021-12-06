import axios from 'axios'

const instance = axios.create({
	baseURL: process.env.API_URL || 'http://localhost:3001/',
	timeout: 5000,
	headers: {}
})

// This allows us to access axios in any context by calling this.$axios
export default (_, inject) => {
	inject('axios', instance)
}
