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

#   Returns an array of all videos for a given user
def videosGet(event, context):
    queryParams = event['queryStringParameters']
    
    if queryParams and 'username' in queryParams:
        username = event['queryStringParameters']['username']
        response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('VIDEO'))
    else:
        scan_kwargs = {
            'FilterExpression': Key('sk').begins_with('VIDEO')
        }
        response = dynamodb.scan(**scan_kwargs) 

    return {
        'statusCode': 200,
        'body': json.dumps({ 'Items': response['Items'] })
    }
    
def videoGet(event, context):
    if 'pk' not in event['queryStringParameters']:
        return badRequest("Error: pk required in request")
    if 'sk' not in event['queryStringParameters']:
        return badRequest('Error: sk required in request')
    
    pk = event['queryStringParameters']['pk']
    sk = event['queryStringParameters']['sk']
    
    response = dynamodb.query(KeyConditionExpression = Key('pk').eq(pk) & Key('sk').eq(sk))
    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

#   Creates a new video
def videosPost(event, context):
    body = json.loads(event['body'])

    #   Assemble video object
    pk = "ID#" + body['username']
    sk = "VIDEO#" + str(uuid.uuid4())
    videoTitle = body['videoTitle']
    videoDescription = body['videoDescription']
    videoKey = body['videoKey'].replace('.mp4', '')
    
    # Put the entry in dynamodb
    response = dynamodb.put_item(
        Item = {
            'pk': pk,
            'sk': sk,
            'videoTitle': videoTitle,
            'videoDescription': videoDescription,
            'videoKey': videoKey
        }
    )

    return {
        'statusCode': 201,
        'body': json.dumps({'response': response})
    }

#   Update a video with given data
def videosPut(event, context):
    body = json.loads(event['body'])

    pk = body['pk']
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

    pk = body['pk']
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