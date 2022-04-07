import boto3
from boto3.dynamodb.conditions import Key
import botocore
import re
import json

def lambda_handler(event, context):
    records = event['Records']
    
    thumbnails = []
    videos = {
        
    }
    
    db_client = boto3.resource('dynamodb').Table('system')

    for record in records:
        BucketKey = record['s3']['object']['key']
        VideoKey = re.search('.+?(?=\/)', BucketKey).group(0)
        ThumbnailKey = BucketKey[len(VideoKey) + 1:]
        
        thumbnails = thumbnails + [ThumbnailKey]
        
        video = {}
        
        if VideoKey in videos:
            video = videos[VideoKey]
        else:
            # Query the expected video
            resp = db_client.query(
                IndexName="videoKey-index",
                KeyConditionExpression=Key('videoKey').eq(VideoKey)
            )
            
            # If the video does not exist, return
            if resp['Count'] <= 0:
                print("Video not found")
                continue
        
            # Get the video
            video = resp['Items'][0]
            
            videos[VideoKey] = video
        
        if 'altThumbnails' in video:
          thumbnails = thumbnails + json.loads(video['altThumbnails'])
        
    if len(thumbnails) == 0:
        return
    
    # Remove duplicates
    thumbnails = list(set(thumbnails))
    
    altThumbnails = json.dumps(thumbnails)
    
    for videoKey, video in videos.items():
      resp = db_client.update_item(
        Key={
            'pk': video['pk'],
            'sk': video['sk']
        },
        UpdateExpression="set altThumbnails=:a",
        ExpressionAttributeValues={
            ':a': altThumbnails
        },
        ReturnValues="UPDATED_NEW"
      )