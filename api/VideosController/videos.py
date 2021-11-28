import boto3
from boto3.dynamodb.conditions import Key
import json
import os

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def videosGet(event, context):
    username = event['queryStringParameters']['username']

    response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').begins_with('VIDEO'))

    return {
        'statusCode': 200,
        'body': json.dumps({ 'Items': response['Items'] })
    }

def videosPost(event, context):
    return {
        'statusCode': 200,
        'body': 'videosPost'
    }

def videosPut(event, context):
    return {
        'statusCode': 200,
        'body': 'videosPut'
    }

def videosDelete(event, context):
    return {
        'statusCode': 200,
        'body': 'videosDelete'
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