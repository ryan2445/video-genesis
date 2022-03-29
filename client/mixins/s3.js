import { PutObjectCommand, DeleteObjectCommand } from "@aws-sdk/client-s3";
import { nanoid } from "nanoid";

export default {
  methods: {
    /*
      @params: 
        bucket -> string
        key -> string
    */
    async s3_delete(bucket, key) {
      try {
        const deletePayload = {
          Bucket: bucket,
          Key: key,
        };
  
        const deleteCommand = new DeleteObjectCommand(deletePayload);
            
        await this.$store.getters["auth/s3"].send(
          deleteCommand
        );
      }
      catch(e) {
        console.log('S3 Delete Error')
        console.error(e)
      }
    },
    /*
      @params: 
        bucket -> string
        key -> string
        body -> File
      @returns:
        key -> string
    */
    async s3_put(bucket, key, body) {
      try {
        // Construct the payload
        const putPayload = {
          Bucket: bucket,
          Key: key,
          Body: body,
          CacheControl: "max-age=31536000"
        };
        
        // Prepare s3 the put command
        const putCommand = new PutObjectCommand(putPayload);

        // Send the put command to s3
        const putResp = await this.$store.getters["auth/s3"].send(putCommand);

        // Construct the url of the uploaded item
        const newKey = `https://${bucket}.s3.us-west-2.amazonaws.com/${putPayload.Key}`;

        return newKey;
      }
      catch(e) {
        console.log('S3 Put Error')
        console.error(e)
      }
    },
    /*
      @params: 
        file -> File
      @returns:
        key -> string
    */
    key_from_file(file) {
      if (!file || !file.type) {
        console.error("File does not have type attribute")
        return
      }

      return this.key_from_string(file.type, true)
    },
    /*
      @params: 
        str -> String
        uuid -> boolean
      @returns:
        key -> string
    */
    key_from_string(str, uuid = false) {
      // Split the string into an arr by '/' delimiter
      const arr = str.split('/')
      
      const key = arr.at(-1);

      return uuid
        ? nanoid() + `.${key}` 
        : key
    }
  },
}