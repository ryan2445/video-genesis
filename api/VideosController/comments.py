from ast import Expression
from urllib import response
from xmlrpc.client import ResponseError
import boto3
from boto3.dynamodb.conditions import Key
import simplejson as json
import ulid
import os

#This part of the code connects to the database
if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

def badRequest(msg):
    return {
        'statusCode': 400,
        'body': msg
    }


def getVideoComments(event, context):
    quearyParams = event['queryStringParameters']
    videoId = quearyParams['videoId']
    response = dynamodb.query(KeyConditionExpression= Key('pk').eq("VIDEO#" + videoId) & Key('sk').begins_with('COMMENT'),  Limit = 10, ScanIndexForward = False)
    
    while 'LastEvluatedKey' in response:
        key = response['LastEvaluatedKey']
        response = dynamodb.query(KeyConditionExpression= Key('pk').eq('VIDEO#' + videoId) & Key('sk').begins_with('COMMENT'),  Limit = 10, ScanIndexForward = False, ExclusiveStartKey=key)
        
        
    return {
        'statusCode': 200,
        'body': json.dumps(response['Items'])
    }

    
def updateUserComment(event, context):
    body = json.loads(event['body'])
    print(body['videoId'])
    pk = body['videoId']
    sk = "COMMENT#" + body['commentId']
    content = body['content']
    
    response = dynamodb.update_item(
        Key={'pk': pk, 'sk': sk}, ExpressionAttributeNames ={ '#c' : 'content'},
        UpdateExpression = 'set #c = :value', 
        ExpressionAttributeValues = {':value' : content})


def createUserComment(event, context):
    body = json.loads(event['body'])
    
    pk = body['videoId']
    sk = "COMMENT#" + ulid.new().str
    userId = event['requestContext']['authorizer']['claims']['cognito:username']
    
    content = body['content']
    
    response = dynamodb.put_item(
        Item = {
            'pk': pk,
            'sk': sk,
            'userId': userId,
            'content': content
        }
    )
    
    return {
        'statusCode': 201,
        'body': json.dumps({'response': response})
    }
    

def deleteUserComment(event, context):
    body = json.loads(event['body'])
    pk = "VIDEO#" + body['videoId']
    sk = "COMMENT#" + body['commentId']
    
    response = dynamodb.delete_item(
        Key = {
            'pk': pk,
            'sk': sk
        }
    )
    
    return {
        'statusCode': 200,
        'body': json({'response': response})
    }


def handle(event, context):
    response = None
    
    methods = {
        'GET': {'/comments': getVideoComments},
        'POST': {'/comments': updateUserComment},
        'PUT': {'/comments': createUserComment},
        'DELETE': {'/comments': deleteUserComment},
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