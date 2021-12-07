import boto3
from boto3.dynamodb.conditions import Key
import json
import os
import uuid
# from mpegdash.parser import MPEGDASHParser

if os.getenv('AWS_SAM_LOCAL'):
    dynamodb = boto3.resource('dynamodb', endpoint_url = 'http://dynamodb-local:8000').Table('system')
else:
    dynamodb = boto3.resource('dynamodb').Table('system')

#   Helper function to get video metadata from a video in S3
# def videoMetadata(videoKey):
#     #   Create the S3 object URL
#     s3URL = "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com/" + videoKey + "/" + videoKey + ".mpd"

#     #   Parse the mpd file at the URL
#     mpd = MPEGDASHParser.parse(s3URL)

#     #   Get the video metadata
#     representations = mpd.periods[0].adaptation_sets[0].representations

#     #   Collect parts of the video metadata
#     metadata = []
#     for i in range(len(representations)):
#         metadata.append({
#             "id": representations[i].id,
#             "width": representations[i].width,
#             "height": representations[i].bandwidth,
#             "codecs": representations[i].codecs,
#             "scanType": representations[i].scan_type,
#             "baseURL": representations[i].base_urls[0].base_url_value
#         })

#     #   Return video metadata
#     return metadata

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

    #   Assemble video object
    pk = "ID#" + body['username']
    sk = "VIDEO#" + str(uuid.uuid4())
    videoTitle = body['videoTitle']
    videoDescription = body['videoDescription']
    videoKey = body['videoKey'].replace('.mp4', '')
    videoUrls = {
        'original': "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com/" + videoKey + "/" + videoKey + ".mp4",
        '325': "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com/" + videoKey + "/" + videoKey + "_325.mp4",
        '750': "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com/" + videoKey + "/" + videoKey + "_750.mp4",
        '1500': "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com/" + videoKey + "/" + videoKey + "_1500.mp4",
        '3000': "https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com/" + videoKey + "/" + videoKey + "_3000.mp4"
    }

    response = dynamodb.put_item(
        Item = {
            'pk': pk,
            'sk': sk,
            'videoTitle': videoTitle,
            'videoDescription': videoDescription,
            'videoKey': videoKey,
            'videoUrls': videoUrls
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