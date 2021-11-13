import boto3
import json
import os

def handle(event, context):
    if os.getenv('AWS_SAM_LOCAL'):
        dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('names')
    else:
        dynamodb = boto3.resource('dynamodb').Table('names')

    method = event['httpMethod']

    if method == 'GET':
        name = event['queryStringParameters']['name']

        response = dynamodb.get_item(Key = { 'name': name })

        return {
            'statusCode': 200,
            'body': json.dumps({ 'response': response })
        }

    if method == 'POST':
        body = event['body']

        body = json.loads(body)

        name = body['name']

        response = dynamodb.put_item(Item = { 'name': name })

        return {
            'statusCode': 200,
            'body': json.dumps({ 'response': response })
        }
    
    return {
        'statusCode': 404,
        'body': 'Not Found'
    }