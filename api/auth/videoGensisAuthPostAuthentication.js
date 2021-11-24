const AWS = require('aws-sdk');
const docClient = new AWS.DynamoDB.DocumentClient();

// The DynamoDB access params
const params = { 
    TableName: 'system'
};

// Sets the DynamoDB access params
const setParams = (event) => {
    params.Key = {
        pk: `ID#${event.userName}`,
        sk: `USER`
    }
};

// Check if the user exists in the DynamoDB table
const getUser = async () => {
    try {
        // Query the database for the user
        const data = await docClient.get(params).promise()
        
        // If the data is empty, the user does not exist and return null
        if (Object.entries(data).length == 0) {
            return null
        }

        // otherwise return the user
        return data
    }
    catch (error) {
        console.log('error in getUser:', error)
    }
    
    // If data was not returned, return nothing
    return null
}

// If the user does not exist, this function creates the user
const createUser = async (event) => {
    // Update the params for create
    const params = {
        TableName: 'system',
        Item: {
            pk: `ID#${event.userName}`,
            sk: 'USER',
            email: event.request.userAttributes.email,
            username: event.userName,
            email_verified: event.request.userAttributes.email_verified
        }
    }
    
    try {
        // Create the user
        const user = await docClient.put(params).promise()

        // Return the user
        return user
    }
    catch(error) {
        console.log('error in user create', error)
    }
}

exports.handler = async (event, context, callback) => {
    // Set the initial params
    setParams(event)
    
    // Get the user
    const user = await getUser()
    
    // If the user does not exist, create the user
    if (!user) {
        await createUser(event)
    }
    
    // Continue to the next cognito callback
    callback(null, event)
};
