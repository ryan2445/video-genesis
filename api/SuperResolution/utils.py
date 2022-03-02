# This file demonstrates use of TensorFlow Hub Module for Enhanced Super Resolution Generative Adversarial Network (by Xintao Wang et.al.)
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
  
  hr_size = (tf.convert_to_tensor(hr_image.shape[:-1]) // 4) * 4
  hr_image = tf.image.crop_to_bounding_box(hr_image, 0, 0, hr_size[0], hr_size[1])
  hr_image = tf.cast(hr_image, tf.float32)
  return tf.expand_dims(hr_image, 0)

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

def downsample_video(video_path = "original.mp4"):
  if not os.path.isfile(video_path):
    raise RuntimeError(f"Unknown file path {video_path}")
  
  output_video = 'lr.mp4'
  
  if os.path.isfile(output_video):
    os.remove(output_video)
  
  cap = cv2.VideoCapture(video_path)
  success, frame = cap.read()
  
  if not success:
    raise RuntimeError("Cannot read video")
  
  scaling_algorithm = "bicubic"
  
  height = frame.shape[0]
  width = frame.shape[1]
  
  command = f'ffmpeg -i "{video_path}" -ss 0 -vf scale={width // 4 }:{height // 4} -sws_flags {scaling_algorithm} -c:a copy "{output_video}"'
  subprocess.call(command, shell=True)

def downscale_image(image):
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

def upscale_video(video_src = "lr.mp4"):
  if not os.path.isfile(video_src):
    raise RuntimeError("Video not found to upscale")

  cap = cv2.VideoCapture(video_src)
  
  if (cap.isOpened() == False):
    raise RuntimeError(f"Could not open {video_src}")
  
  success, frame = cap.read()
  height = frame.shape[0]
  width = frame.shape[1]
  fps = cap.get(cv2.CAP_PROP_FPS)
  frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  output_video_path="hr.mp4"
  dir = 'temp'
  path = dir + "/temp.jpeg"
  model = load_model()

  if not os.path.isdir(dir):
    os.mkdir(dir)
  
  if os.path.isfile(path):
    os.remove(path)
    
  if os.path.isfile(output_video_path):
    os.remove(output_video_path)
    
  out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'MP4V'), fps, (width * 4, height * 4))
  
  for i in tqdm(range(frames_count - 1)):
    if success is False:
      break
    
    lr_image = preprocess_image_from_cv(frame)
    fake_image = model(lr_image)
    fake_image = tf.squeeze(fake_image)
    fake_image = np.asarray(fake_image)
    fake_image = tf.clip_by_value(fake_image, 0, 255)
    fake_image = tf.cast(fake_image, tf.uint8).numpy()
    
    cv2.imshow('Read', frame)
    cv2.imshow('Write', fake_image)
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break
    out.write(fake_image)
    success, frame = cap.read()
  
  cap.release()
  out.release()
  
# downscale_video("https://genesis2vod-staging-output-q1h5l756.s3.us-west-2.amazonaws.com/-xZxpyDAoWDinJf52gu9j/-xZxpyDAoWDinJf52gu9j_3000.mp4")
# upscale_video()

# test()
downsample_video()
upscale_video()