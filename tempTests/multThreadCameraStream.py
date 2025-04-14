#v4l2-ctl --list-devices
#ffplay rstp://address:port/mystream
#list video devices
from datetime import datetime
from time import sleep, time
import sys
import os
import cv2
import numpy as np
from picamera2 import Picamera2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.CameraImageConnector import ImageConnector
from utils.ThreadingCamera import loadCameras


fps = 15
width = 1280
height = 720
colors = [
    (0, 0, 255),
    (255, 0, 0),
    (0, 255, 0),
]

out = cv2.VideoWriter('appsrc ! videoconvert' + \
    ' ! video/x-raw,format=I420' + \
    ' ! x264enc speed-preset=ultrafast bitrate=2000 key-int-max=' + str(fps * 2) + \
    ' ! video/x-h264,profile=baseline' + \
    ' ! rtspclientsink location=rtsp://192.168.2.110:8554/mystream',
    #' ! webrtcclientsink location=ws://192.168.2.134:8000/mystream',
    cv2.CAP_GSTREAMER, 0, fps, (width*2, height*2), True)
if not out.isOpened():
    raise Exception("can't open video writer")

curcolor = 0
start = time()

cameras = {"Camera1": (0, (height,width)), "Camera2": (1,(height,width)), "Camera3": (2,(height,width)), "Camera4": (3,(height,width))}

print(cameras.values())

camerasLoaded = loadCameras(cameras.values())
frames = []
imageConnector = ImageConnector(width,height)
print(camerasLoaded)
if not camerasLoaded:
    print(camerasLoaded)
    print("Error loading cameras")
    exit()

print('setup gotowy')
while True:
    frames = [frame.getFrame() for frame in camerasLoaded]
    #print(camerasLoaded[0].getFrame())
    imageConnector.setImages(frames)
    if imageConnector.connectImagesSquare(2):
        image = imageConnector.getConnectedImage()
        if image is not None:
            out.write(image)
        else:
            print("Error getting connected image")
            continue
    else:
        print("Error connecting frames")
        print("Frame skipped")
        continue
