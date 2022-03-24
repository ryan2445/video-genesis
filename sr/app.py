from flask import Flask, request, abort
import werkzeug
from SuperResolution import utils

app = Flask(__name__)

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
  
  utils.download_file(body['video_url'], "SuperResolution/files", "original.mp4")
  utils.downsample_video("SuperResolution/files/original.mp4", "SuperResolution/files/lr.mp4")
  utils.upscale_video("SuperResolution/files/lr.mp4", "SuperResolution/files/hr.mp4")
  
  return "Success"

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handleBadRequest(e):
  return 'Bad Request', 400