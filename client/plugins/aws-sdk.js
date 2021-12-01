var AWS = require('aws-sdk')
var myCredentials = new AWS.CognitoIdentityCredentials({IdentityPoolId:'us-west-2:a7e3dcf8-8ead-4d2f-b0c5-c9b2fca24109'});
var myConfig = new AWS.Config({
  credentials: myCredentials, 
  region: 'us-west-2'
});

export default (_, inject) => {
    inject('aws', AWS)
    inject('aws_credentials', myCredentials)
    inject('aws_config', myConfig)
}