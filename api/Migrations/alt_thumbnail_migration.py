import boto3
from boto3.dynamodb.conditions import Key
import re
import json

def main():
  s3 = boto3.resource('s3')
  bucket = s3.Bucket('videogenesis-thumbnails')
  db_client = boto3.resource('dynamodb').Table('system')
  
  videos =  {
    
  }
  
  for object in bucket.objects.all():
    Key = object.key
    VideoKey = re.search('.+?(?=\/)', Key).group(0)
    ThumbnailKey = Key[len(VideoKey) + 1:]
    
    print(VideoKey)
    
    if VideoKey not in videos:
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
      
      # Save the video in memo
      videos[VideoKey] = video
    
    thumbnails = []
    
    if 'altThumbnails' in videos[VideoKey]:
      thumbnails = thumbnails + json.loads(videos[VideoKey['altThumbnails']])

    thumbnails = thumbnails + [ThumbnailKey]
    
    thumbnails = list(set(thumbnails))
      
    thumbnails = json.dumps(thumbnails)
    
    VideoKey['altThumbnails'] = thumbnails
    
  for videoKey, video in videos.items():
    resp = db_client.update_item(
      Key={
          'pk': video['pk'],
          'sk': video['sk']
      },
      UpdateExpression="set altThumbnails=:a",
      ExpressionAttributeValues={
          ':a': video['altThumbnails']
      },
      ReturnValues="UPDATED_NEW"
    )
    print('Updated', videoKey)
  
  return None


if __name__ == '__main__':
  main()