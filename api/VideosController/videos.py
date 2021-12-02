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

    response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('VIDEO'))

    return {
        'statusCode': 200,
        'body': json.dumps({ 'Items': response['Items'] })
    }

#   Creates a new video
def videosPost(event, context):
    body = json.loads(event['body'])

    pk = "ID#" + body['username']
    sk = "VIDEO#" + str(uuid.uuid4())
    videoTitle = body['videoTitle']

    response = dynamodb.put_item(
        Item = {
            'pk': pk,
            'sk': sk,
            'videoTitle': videoTitle
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

    if method == 'GET':
        return videosGet(event, context)
    elif method == 'POST':
        return videosPost(event, context)
    elif method == 'PUT':
        return videosPut(event, context)
    elif method == 'DELETE':
        return videosDelete(event, context)

    return {
        'statusCode': 404,
        'body': 'Not Found'
    }