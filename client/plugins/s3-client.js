const REGION = "us-west-2";
const INPUT_BUCKET = 'genesis2vod-staging-input-q1h5l756'
const OUTPUT_BUCKET = 'genesis2vod-staging-output-q1h5l756'

import {
    GetObjectCommand,
    ListObjectsCommand,
    PutObjectCommand,
    S3Client,
} from "@aws-sdk/client-s3";

const filenameGenerator = (key) => {
    const name = key.split("/")[1]
    return { name, encoded: name.replace(/\s+|[\d,/.()]/g, "-") };
}

const { CognitoIdentityClient } = require("@aws-sdk/client-cognito-identity");
const { fromCognitoIdentityPool } = require("@aws-sdk/credential-provider-cognito-identity");

const s3 = new S3Client({
  region: REGION,
  credentials: fromCognitoIdentityPool({
    client: new CognitoIdentityClient({ region: REGION }),
    identityPoolId: "us-west-2:a7e3dcf8-8ead-4d2f-b0c5-c9b2fca24109",
  }),
});

const uploadFn = async (credentials) => {
    const files = document.querySelector("#input-upload").files
  
    if (!files.length) return alert("Please choose a file to upload first!")
  
    try {
      const file = files[0]
      const fileName = file.name
  
      const s3Client = new S3Client({
        region,
        credentials,
      })
  
      await s3Client.send(
        new PutObjectCommand({
          Bucket: bucket,
          Key: `${credentials.identityId}/${fileName}`,
          Body: file,
          ContentType: 'mp4',
        })
      )
  
      alert("Uploaded successful!")
      window.location.reload()
    } catch (err) {
      alert(err.message)
  
      window.location = "http://localhost:3000"
    }
  }
  


export default (_, inject) => {
    console.log(process.env)
    inject('s3', s3)
}