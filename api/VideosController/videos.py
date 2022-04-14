import boto3
from boto3.dynamodb.conditions import Key
import simplejson as json
import os
import uuid
import sys

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def badRequest(msg: str) -> dict:
    return {
        'statusCode': 400,
        'body': msg
    }

#   Returns an array of all videos for a given user
def videosGet(event, context):
    queryParams = event['queryStringParameters']
    
    if queryParams and 'username' in queryParams:
        username = event['queryStringParameters']['username']
        response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('VIDEO'))
    else:
        scan_kwargs = {
            'FilterExpression': Key('sk').begins_with('VIDEO') & Key('isPrivate').eq(False)
        }
        response = dynamodb.scan(**scan_kwargs)
    
    # Init a dict to map users
    userMap = {}

    def addUser(video):
        pk = video['pk']
        if pk in userMap:
            video["user"] = userMap[pk]
        else:
            # Get the user
            user = dynamodb.query(KeyConditionExpression = Key('pk').eq(pk) & Key('sk').eq('USER'), Limit=1)
            # If the user exists, attach them to the video
            if (user["Count"] >= 1):
                video["user"] = user["Items"][0]
                userMap[pk] = user["Items"][0]
        return video
    
    # Add the user to each video
    response = [addUser(v) for v in response['Items']]

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
    
def videoGet(event, context):
    if 'pk' not in event['queryStringParameters']:
        return badRequest("Error: pk required in request")
    if 'sk' not in event['queryStringParameters']:
        return badRequest('Error: sk required in request')
    
    pk = event['queryStringParameters']['pk']
    sk = event['queryStringParameters']['sk']
    
    # Get the video
    video = dynamodb.query(KeyConditionExpression = Key('pk').eq(pk) & Key('sk').eq(sk), Limit=1)

    # If the video does not exist, return bad request
    if (video["Count"] == 0):
        badRequest("Video does not exist")
    
    # Initialize the response
    response = video["Items"][0]
    
    # Get the user who uploaded the video
    user = dynamodb.query(KeyConditionExpression = Key('pk').eq(pk) & Key('sk').eq('USER'), Limit=1)
    
    # If the user exists, attach them to the video
    if (user["Count"] == 1):
        response["user"] = user["Items"][0]
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

#   Creates a new video
def videosPost(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']

    #   Assemble video object
    pk = "ID#" + userId
    sk = "VIDEO#" + str(uuid.uuid4())
    videoTitle = body['videoTitle']
    videoDescription = body['videoDescription']
    videoKey = body['videoKey'].replace('.mp4', '')
    isPrivate = body.get('isPrivate', False)
    
    payload = {
        'pk': pk,
        'sk': sk,
        'videoTitle': videoTitle,
        'videoDescription': videoDescription,
        'videoKey': videoKey,
        'isPrivate': isPrivate
    }
    
    # Put the entry in dynamodb
    response = dynamodb.put_item(
        Item = payload
    )

    return {
        'statusCode': 201,
        'body': json.dumps(payload)
    }

#   Update a video with given data
def videosPut(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']

    pk = "ID#" + userId
    sk = body['sk']
    optional_keys = [
        'videoTitle',
        'videoDescription',
        'videoThumbnail'
    ]

    keys = list(filter(lambda x: body.get(x), optional_keys))
    if not keys: return badRequest("No attributes to update.")

    update_keys = []
    update_attributes = []
    for index, key in enumerate(keys):
        update_keys.append(f"{key}=:{index}")
        update_attributes.append((f":{index}", body.get(key)))
    
    response = dynamodb.update_item(
        Key = { 'pk': pk, 'sk': sk },
        UpdateExpression = f"set {', '.join(update_keys)}",
        ExpressionAttributeValues = dict(update_attributes)
    )

    return {
        'statusCode': 200,
        'body': json.dumps({ 'response': response })
    }

#   Deletes some attributes based on a primary key and sort key
def videosDelete(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']

    pk = "ID#" + userId
    sk = body['sk']

    response = dynamodb.delete_item(
        Key = {
            'pk': pk,
            'sk': sk
        }
    )
    
    # Query the user's playlists    
    playlistItemsQuery = dynamodb.scan(
        FilterExpression = Key('videoPK').eq(pk) & Key('videoSK').eq(sk)
    )
    
    if playlistItemsQuery['Count'] > 0:
        for item in playlistItemsQuery['Items']:
            dynamodb.delete_item(
                Key = { 'pk': item['pk'], 'sk': item['sk'] }
            )

    return {
        'statusCode': 200,
        'body': json.dumps({ 'response': response })
    }

def handle(event, context):
    response = None
    
    methods = {
        'GET': {
            '/videos/all': videosGet,
            '/videos': videoGet
        },
        'POST': {
            '/videos': videosPost
        },
        'PUT': {
            '/videos': videosPut
        },
        'DELETE': {
            '/videos': videosDelete
        }
    }
    
    method = event['httpMethod']
    path = event['path']
    
    response = methods[method][path](event, context)

    if not response:
        response = {
            'statusCode': 404,
            'body': 'Not Found'
        }

    response['headers'] = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    return response
