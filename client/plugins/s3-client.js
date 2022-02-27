import { S3Client } from "@aws-sdk/client-s3"

const { fromCognitoIdentityPool } = require("@aws-sdk/credential-providers")

const REGION = "us-west-2"

export default async ({ $auth }, inject) => {
	var session = await $auth.currentSession()

	var identity = session.getIdToken()

	var token = identity.getJwtToken()

	const s3 = new S3Client({
		region: REGION,
		credentials: fromCognitoIdentityPool({
			clientConfig: { region: REGION },
			identityPoolId: "us-west-2:a7e3dcf8-8ead-4d2f-b0c5-c9b2fca24109",
			logins: {
				"cognito-idp.us-west-2.amazonaws.com/us-west-2_3LjdLzhH5": token
			}
		})
	})

	inject("s3", s3)
}
