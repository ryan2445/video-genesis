from asyncio.windows_events import NULL
import boto3
from boto3.dynamodb.conditions import Key
import json
import os
import uuid

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

#   Returns an array of all videos for a given user
def videosGet(event, context):
    username = event['queryStringParameters']['username']

    if username:
        response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('VIDEO'))
    else:
        response = dynamodb.query(KeyConditionExpression =Key('sk').begins_with('VIDEO'))

    return {
        'statusCode': 200,
        'body': json.dumps({ 'Items': response['Items'] })
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
        'statusCode': 200,
        'body': json.dumps({'response': response})
    }

#   Update a video with given data
def videosPut(event, context):
    body = json.loads(event['body'])

    pk = body['pk']
    sk = body['sk']
    videoTitle = body['videoTitle']

    response = dynamodb.update_item(
        Key = {
            'pk': pk,
            'sk': sk
        },
        UpdateExpression = 'set videoTitle=:0',
        ExpressionAttributeValues = {
            ':0': videoTitle
        }
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
    method = event['httpMethod']

    response = None

    if method == 'GET':
        response = videosGet(event, context)
    elif method == 'POST':
        response = videosPost(event, context)
    elif method == 'PUT':
        response = videosPut(event, context)
    elif method == 'DELETE':
        response = videosDelete(event, context)

    if not response:
        response = {
            'statusCode': 404,
            'body': 'Not Found'
        }

    response['headers'] = {
        'Access-Control-Allow-Origin': '*'        
    }

    return response