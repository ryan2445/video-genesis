import Amplify, { Auth } from 'aws-amplify';
import awsconfig from '../aws-exports.js';
Amplify.configure(awsconfig);

import { Hub, Logger } from 'aws-amplify';

const logger = new Logger('Auth');

const listener = data => {
			console.log('WTF IS THIS', data.payload)
	switch (data.payload.event) {
		case 'signIn':
			window.mitt.emit('SIGN_IN');
			logger.info('user signed in');
			break
		case 'signUp':
			logger.info('user signed up')
			break
		case 'signOut':
			logger.info('user signed out')
			break
		case 'signIn_failure':
			logger.error('user sign in failed')
			break
		case 'tokenRefresh':
			window.mitt.emit('TOKEN_REFRESH')
			logger.info('token refresh succeeded')
			break
		case 'tokenRefresh_failure':
			logger.error('token refresh failed')
			break
		case 'configured':
			logger.info('the Auth module is configured')
	}
}

Hub.listen('auth', listener)

// This allows us to access Auth in any context by calling this.$auth
export default (_, inject) => {
	inject('auth', Auth)
}
