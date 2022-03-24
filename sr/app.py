from flask import Flask, request, abort
import werkzeug
from SuperResolution import utils
import boto3
from boto3.dynamodb.conditions import Key

app = Flask(__name__)
dynamo = boto3.resource('dynamodb').Table('system')
s3 = boto3.client('s3')

@app.route("/")
def index():
  return "<p>SR Server is Running!</p>"

@app.route("/process", methods=['POST'])
def process():
  body = request.get_json()
  
  if 'video_url' not in body:
    abort(400)
  if 'video_key' not in body:
    abort(400)
  
  # Query the DB for the video based on the videoKey
  resp = dynamo.query(
    IndexName="videoKey-index",
    KeyConditionExpression=Key('videoKey').eq(body['video_key'])
  )
  
  # If no videos returned, abort
  if not resp or resp['Count'] == 0:
    abort(401)
  
  # Get the video
  video = resp['Items'][0]
  
  if 'videoData' not in video:
    return 'Video not yet uploaded', 401
  
  filePath = "SuperResolution/files"
  lrPath = f"{filePath}/lr.mp4"
  hrPath = f"{filePath}/hr.mp4"
  ogPath = f"{filePath}/original.mp4"
  
  # Download the video
  utils.download_file(body['video_url'], filePath, "original.mp4")
  
  # Downsample the video
  utils.downsample_video(ogPath, lrPath)
  
  # Upscale the video
  utils.upscale_video(lrPath, hrPath)
  
  # Assemble Payload for LR and HR video
  bucket = "genesis2vod-staging-output-q1h5l756"
  key = body['video_key']
  
  # Load the downsampled video
  lr = open('SuperResolution/files/lr.mp4', 'rb')
  
  # Upload the downsampled video
  resp = s3.put_object(
    Body=lr,
    Bucket=bucket,
    Key=f'{key}/lr.mp4'
  )
  
  lr.close()
  
  # Load the fake video
  hr = open('SuperResolution/files/hr.mp4', 'rb')
  
  # Upload the fake video
  resp = s3.put_object(
    Body=hr,
    Bucket=bucket,
    Key=f'{key}/hr.mp4'
  )
  
  hr.close()
  
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
  
  return "Success"

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handleBadRequest(e):
  return 'Bad Request', 400