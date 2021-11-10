import Amplify, { Auth } from 'aws-amplify';
import awsconfig from '../aws-exports';
Amplify.configure(awsconfig);

// This allows us to access Auth in any context by calling this.$auth
export default (_, inject) => {
    inject('auth', Auth)
}