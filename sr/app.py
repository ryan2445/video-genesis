from flask import Flask, request, abort
import werkzeug
from SuperResolution import utils
import boto3
from boto3.dynamodb.conditions import Key
from rq import Queue
from rq.job import Job
from worker import conn
from service import processVideo
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
dynamo = boto3.resource('dynamodb').Table('system')
s3 = boto3.client('s3')
queue = Queue(connection=conn, default_timeout=6000)

@app.route("/")
def index():
  return "SR Server is Running!"

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
    print('here')
    return 'Video not yet uploaded', 401
  
  if 'lrBaseURL' in video and 'hrBaseURL' in video:
    return "Video already processed"
  
  job = queue.enqueue_call(
    func=processVideo, args=(video, body['video_url'], body['video_key'],), result_ttl=86400
  )
  
  print(job.get_id())
  
  return "Success"

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handleBadRequest(e):
  return 'Bad Request', 400