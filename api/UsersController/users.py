import boto3
from boto3.dynamodb.conditions import Key
import json
import os

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def badRequest(msg: str) -> dict:
    return {
        'statusCode': 400,
        'body': msg
    }

def usersGet(event, context):
    username = event['queryStringParameters']['username']
    response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').eq("USER"))

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def usersPut(event, context):
    body = json.loads(event['body'])

    pk = body['pk']
    sk = body['sk']
    optional_keys = [
        'usersFirstName',
        'usersLastName',
        'usersAboutMe',
        'profilePicKey',
        'coverPicKey'
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

def handle(event, context):
    response = None

    methods = {
        'GET': {
            '/users/all': usersGet
        },
        'PUT': {
            '/users': usersPut
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