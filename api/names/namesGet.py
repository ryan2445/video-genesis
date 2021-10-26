import boto3
import json
import os

def handle(event, context):
    if os.getenv("AWS_SAM_LOCAL"):
        dynamodb = boto3.resource('dynamodb', endpoint_url = "http://dynamodb-local:8000").Table('names')
    else:
        dynamodb = boto3.resource('dynamodb').Table('names')

    name = event['pathParameters']['name']

    response = dynamodb.get_item(Key = { 'name': name })

    return {
        "statusCode": 200,
        "body": json.dumps({ "response": response })
    }