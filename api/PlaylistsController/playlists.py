import boto3
from boto3.dynamodb.conditions import Key
import simplejson as json
import os
import uuid

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def badRequest(msg: str) -> dict:
    return {
        'statusCode': 400,
        'body': msg
    }

#   Returns an array of all playlists for a given user
def playlistsGet(event, context):
    queryParams = event['queryStringParameters']
    
    if queryParams and 'username' in queryParams:
        username = event['queryStringParameters']['username']
        response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('playlist'))
    else:
        scan_kwargs = {
            'FilterExpression': Key('sk').begins_with('playlist') & Key('isPrivate').eq(False)
        }
        response = dynamodb.scan(**scan_kwargs) 

    return {
        'statusCode': 200,
        'body': json.dumps({ 'Items': response['Items'] })
    }
    
def playlistGet(event, context):
    if 'pk' not in event['queryStringParameters']:
        return badRequest("Error: pk required in request")
    if 'sk' not in event['queryStringParameters']:
        return badRequest('Error: sk required in request')
    
    pk = event['queryStringParameters']['pk']
    sk = event['queryStringParameters']['sk']
    
    response = dynamodb.query(KeyConditionExpression = Key('pk').eq(pk) & Key('sk').eq(sk) )
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

#   Creates a new playlist
def playlistsPost(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']

    #   Assemble playlist object
    pk = "ID#" + userId
    sk = "playlist#" + str(uuid.uuid4())
    playlistTitle = body['playlistTitle']
    videos = body.get(videos, [])
    isPrivate = body.get('isPrivate', False)
    
    # Put the entry in dynamodb
    response = dynamodb.put_item(
        Item = {
            'pk': pk,
            'sk': sk,
            'playlistTitle': playlistTitle,
            'videos': videos,
            'isPrivate': isPrivate
        }
    )

    return {
        'statusCode': 201,
        'body': json.dumps({'response': response})
    }

#   Update a playlist with given data
def playlistsPut(event, context):
    body = json.loads(event['body'])
    userId = event['requestContext']['authorizer']['claims']['cognito:username']

    pk = "ID#" + userId
    sk = body['sk']
    optional_keys = [
        'playlistTitle',
        'videos',
        'playlistThumbnail'
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
def playlistsDelete(event, context):
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

    return {
        'statusCode': 200,
        'body': json.dumps({ 'response': response })
    }
def getPlaylistsByVideo(event, context):
    queryParams = event['queryStringParameters']
    
    if queryParams and 'username' in queryParams and 'video' in queryParams:
        username = event['queryStringParameters']['username']
        video = event['queryStringParameters']['video']
        response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('playlist') & Key('videos').contains(video))
    else:
        scan_kwargs = {
            'FilterExpression': Key('sk').begins_with('playlist') & Key('isPrivate').eq(False)
        }
        response = dynamodb.scan(**scan_kwargs) 

    return {
        'statusCode': 200,
        'body': json.dumps({ 'Items': response['Items'] })
    }
    


def handle(event, context):
    response = None
    
    methods = {
        'GET': {
            '/playlists/all': playlistsGet,
            '/playlists': playlistGet,
            '/playlists/video': getPlaylistsByVideo 
        },
        'POST': {
            '/playlists': playlistsPost
        },
        'PUT': {
            '/playlists': playlistsPut
        },
        'DELETE': {
            '/playlists': playlistsDelete
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