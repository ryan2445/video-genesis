import boto3
from boto3.dynamodb.conditions import Key
import json
import os
import uuid

def badRequest(msg: str) -> dict:
    return {
        'statusCode': 400,
        'body': msg
    }

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')




def usersGet(event, context):
    queryParams = event['queryStringParameters']
    
    if queryParams is not None and 'username' in queryParams:
        username = event['queryStringParameters']['username']
        response = dynamodb.query(KeyConditionExpression = Key('pk').eq('ID#' + username) & Key('sk').eq("USER"))
    # else:
    #     scan_kwargs = {
    #         'FilterExpression': Key('sk').begins_with('VIDEO')
    #     }
    #     response = dynamodb.scan(**scan_kwargs) 

    return {
        'statusCode': 200,
        'body': json.dumps({ 'Items': response['Items'] })
    }





def usersPut(event, context):
    body = json.loads(event['body'])

    pk = body['pk']
    sk = body['sk']
    # videoTitle = body['videoTitle']
    # videoDescription = body['videoDescription']
    
    params = [
        'usersFirstName',
        'usersLastName',
        'usersAboutMe',
        'profilePicKey',
        'coverPicKey'
    ]

    keys_with_value = list(filter(lambda x: body.get(x), params))
    update_expr = " ".join([f"{key}=:{index}" for index, key in enumerate(keys_with_value)])

    expr_attrib_values = dict((f":{index}", body.get(key)) for index, key in enumerate(keys_with_value))
    
    response = dynamodb.update_item(
        Key = {
            'pk': pk,
            'sk': sk
        },
        UpdateExpression = f"set {update_expr}",
        ExpressionAttributeValues = expr_attrib_values
    )

    return {
        'statusCode': 200,
        'body': json.dumps({ 'response': response })
    }


def handle(event, context):
    response = None
    
    methods = {
        'GET': {
            '/users': usersGet
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
        'Access-Control-Allow-Origin': '*'        
    }

    return response