# This file demonstrates use of TensorFlow Hub Module for Enhanced Super Resolution Generative Adversarial Network (by Xintao Wang et.al.)
from pickle import FALSE
import subprocess, os
import time
from PIL import Image
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib.pyplot as plt
from config import SAVED_MODEL_PATH
import cv2
import requests
from tqdm import tqdm
os.environ["TFHUB_DOWNLOAD_PROGRESS"] = "True"

def load_model(path=SAVED_MODEL_PATH):
  model = hub.load(SAVED_MODEL_PATH)
  return model

def preprocess_image(image_path):
  """ Loads image from path and preprocesses to make it model ready
      Args:
        image_path: Path to the image file
  """
  
  hr_image = tf.image.decode_image(tf.io.read_file(image_path))
  
  # If PNG, remove the alpha channel. The model only supports
  # images with 3 color channels.
  if hr_image.shape[-1] == 4:
    hr_image = hr_image[...,:-1]
  
  return preprocess_image_from_cv(hr_image)

def preprocess_image_from_cv(image):
  """ Loads image from numpy and preprocesses to make it model ready
      Args:
        image: numpy representation of image
  """
  
  hr_size = (tf.convert_to_tensor(image.shape[:-1]) // 4) * 4
  image = tf.image.crop_to_bounding_box(image, 0, 0, hr_size[0], hr_size[1])
  image = tf.cast(image, tf.float32)
  
  return tf.expand_dims(image, 0)

def downscale_video(video_src):
  video_path = "original.mp4"
  if os.path.isfile(video_path):
    os.remove(video_path)
  
  r = requests.get(video_src, allow_redirects=True)
  open(video_path, 'wb').write(r.content)
  
  cap = cv2.VideoCapture(video_path)
  
  if (cap.isOpened() == False):
    print(f"error opening video stream:\n {video_src}")
    return None

  dir = 'temp'
  path = dir + "/temp.jpeg"
  output_video_path = 'lr.mp4'
  
  if not os.path.isdir(dir):
    os.mkdir(dir)
  
  if os.path.isfile(path):
    os.remove(path)
    
  if os.path.isfile(output_video_path):
    os.remove(output_video_path)
  
  success, frame = cap.read()
  height = frame.shape[0]
  width = frame.shape[1]
  fps = cap.get(cv2.CAP_PROP_FPS)
  frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  
  out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (width // 4, height // 4))
  
  for i in tqdm(range(frames_count)):
    if success is False:
      break
    hr_image = preprocess_image_from_cv(frame)
    lr_image = downscale_image(tf.squeeze(hr_image))
    
    final = tf.squeeze(lr_image)
    final = np.asarray(final)
    final = tf.cast(final, tf.uint8).numpy()
    
    out.write(final)
    success, frame = cap.read()
  
  cap.release()
  out.release()
    
  return None

def downsample_video(input_path = "original.mp4", output_path = "lr.mp4"):
  # Ensure the video_path is a valid file
  if not os.path.isfile(input_path):
    raise RuntimeError(f"Unknown file path {input_path}")
  
  # If the output path is a file, remove it
  if os.path.isfile(output_path):
    os.remove(output_path)
  
  # Capture the first frame of the video
  cap = cv2.VideoCapture(input_path)
  success, frame = cap.read()
  
  # If the first frame cannot be captured, raise a runtime error
  if not success:
    raise RuntimeError("Cannot read video")
  
  # Set the params for the ffmpeg command
  height = frame.shape[0]
  width = frame.shape[1]
  scale_factor = 4
  scaling_algorithm = "bicubic" # Chose a different scaling algorithm here: https://ffmpeg.org/ffmpeg-scaler.html
  
  command = f'ffmpeg -i "{input_path}" -vf scale=ceil({width // scale_factor}/2)*2:ceil({height // scale_factor}/2)*2 -sws_flags {scaling_algorithm} -c:a copy "{output_path}"'
  subprocess.call(command, shell=True)

def downscale_image(image):
  #! Depricated for videos, use downsample_video instead
  
  image_size = []
  if len(image.shape) == 3:
    image_size = [image.shape[1], image.shape[0]]
  else:
    raise ValueError("Dimension mismatch. Can work only on single image.")

  image = tf.squeeze(
      tf.cast(
          tf.clip_by_value(image, 0, 255), tf.uint8))

  lr_image = np.asarray(
    Image.fromarray(image.numpy())
    .resize([image_size[0] // 4, image_size[1] // 4],
              Image.BICUBIC))

  lr_image = tf.expand_dims(lr_image, 0)
  lr_image = tf.cast(lr_image, tf.float32)
  return lr_image

def upscale_video(input_path = "lr.mp4", output_path = "h4.mp4", debug = False):
  # Ensure the input_path is a valid file
  if not os.path.isfile(input_path):
    raise RuntimeError("Video must be a file to upscale")

  # Init. the video capture stream
  cap = cv2.VideoCapture(input_path)
  
  # If the capture is not opened, raise an error
  if (cap.isOpened() == False):
    raise RuntimeError(f"Could not open {input_path}")
  
  # Begin reading the video
  success, frame = cap.read()
  
  # If the first frame cannot be read, raise a runtime error
  if success is False:
    raise RuntimeError("Could not read first frame")

  # Loads the model
  model = load_model()
  
  # Removes any old files
  if os.path.isfile(output_path):
    os.remove(output_path)
  
  # Process one frame to get exact height and width of output
  lr_image = preprocess_image_from_cv(frame)
  fake_image = model(lr_image)
  fake_image = postprocess_image(fake_image)
  
  # Create the video write stream
  height = fake_image.shape[0]
  width = fake_image.shape[1]
  fps = cap.get(cv2.CAP_PROP_FPS)
  fourcc = cv2.VideoWriter_fourcc(*'mp4v')
  out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
  
  # Count the number of frames for progress loading
  frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  
  # Iterate over every frame, predict the super-resolution image, and write to video
  print("Starting video upscaling...")
  for i in tqdm(range(frames_count - 1)):
    if success is False:
      break
    
    # Prepare frame for model
    lr_image = preprocess_image_from_cv(frame)
    
    # Generate the image
    fake_image = model(lr_image)
    
    # Postprocess
    fake_image = postprocess_image(fake_image)
    
    # Output to video file
    out.write(fake_image)
    
    # If debug enabled, show input and output images live
    if debug:
      cv2.imshow('Read', frame)
      cv2.imshow('Write', fake_image)
      if cv2.waitKey(25) & 0xFF == ord('q'):
        break

    success, frame = cap.read()
  
  cap.release()
  out.release()
  
  print(f"Proccessed {input_path} to higher resolution to {output_path}")

def postprocess_image(image):
  image = tf.squeeze(image)
  image = np.asarray(image)
  image = tf.clip_by_value(image, 0, 255)
  image = tf.cast(image, tf.uint8).numpy()
  
  return image

def download_file(url, path, name):
  # Get the path to output the bytes
  full_path = os.path.join(path, name)
  
  # Download the file
  r = requests.get(url, allow_redirects=True)
  
  # Write the contents to the path
  open(full_path, 'wb').write(r.content)

# download_file("https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com/3LqQwB0qpB8ZyaQYyqYah/3LqQwB0qpB8ZyaQYyqYah_3000.mp4", "", "original.mp4")
downsample_video(input_path = "original.mp4", output_path = "lr.mp4")
upscale_video(input_path = "lr.mp4", output_path= "hr.mp4", debug = True)