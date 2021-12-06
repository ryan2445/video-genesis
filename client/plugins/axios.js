import axios from 'axios'

const instance = axios.create({
	baseURL: process.env.API_URL || 'http://localhost:3001/', //Prod db url: https://zkcsvdswr2.execute-api.us-west-2.amazonaws.com/Prod/
	timeout: 5000,
	headers: {}
})

// This allows us to access axios in any context by calling this.$axios
export default (_, inject) => {
	inject('axios', instance)
}
