from SuperResolution import utils
import boto3
from boto3.dynamodb.conditions import Key

dynamo = boto3.resource('dynamodb').Table('system')
s3 = boto3.client('s3')

def processVideo(video, video_url, video_key):
  # Indicate that the video is currently being processed
  response = dynamo.update_item(
    Key={
      'pk': video['pk'],
      'sk': video['sk']
    },
    UpdateExpression="set srProcessing=:s",
    ExpressionAttributeValues={
      ':s': True,
    },
    ReturnValues="UPDATED_NEW"
  )
    
  filePath = "SuperResolution/files"
  lrPath = f"{filePath}/lr.mp4"
  hrPath = f"{filePath}/hr.mp4"
  ogPath = f"{filePath}/original.mp4"
  finalPath = f"{filePath}/out.mp4"
  
  # Download the video
  utils.download_file(video_url, filePath, "original.mp4")
  
  # Downsample the video
  utils.downsample_video(ogPath, lrPath)
  
  # Upscale the video
  utils.upscale_video(lrPath, hrPath)
  
  # Compress the upscaled video
  utils.compressMP4(hrPath, finalPath)
  
  # Assemble Payload for LR and HR video
  bucket = "genesis2vod-staging-output-q1h5l756"
  key = video_key
  
  # Load the downsampled video
  lr = open(lrPath, 'rb')
  
  # Upload the downsampled video
  resp = s3.put_object(
    Body=lr,
    Bucket=bucket,
    Key=f'{key}/lr.mp4'
  )
  
  lr.close()
  
  # Load the fake video
  hr = open(finalPath, 'rb')
  
  # Upload the fake video
  resp = s3.put_object(
    Body=hr,
    Bucket=bucket,
    Key=f'{key}/hr.mp4'
  )
  
  hr.close()
  
  utils.cleanUp([lrPath, hrPath, ogPath, finalPath])
  
  response = dynamo.update_item(
    Key={
      'pk': video['pk'],
      'sk': video['sk']
    },
    UpdateExpression="set lrBaseURL=:l, hrBaseURL=:h",
    ExpressionAttributeValues={
      ':l': 'lr.mp4',
      ':h': 'hr.mp4'
    },
    ReturnValues="UPDATED_NEW"
  )
  
  return 'Success'