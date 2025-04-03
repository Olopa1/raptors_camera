from datetime import datetime
from time import sleep, time
import sys
import os
import cv2
import numpy as np
from picamera2 import Picamera2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.CameraImageConnector import ImageConnector



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
    ' ! x264enc speed-preset=ultrafast bitrate=600 key-int-max=' + str(fps * 2) + \
    ' ! video/x-h264,profile=baseline' + \
    ' ! rtspclientsink location=rtsp://192.168.2.110:8554/mystream',
  #  ' ! webrtcclientsink location=ws://192.168.1.134:8000/mystream',
    cv2.CAP_GSTREAMER, 0, fps, (width*2, height*2), True)
if not out.isOpened():
    raise Exception("can't open video writer")

curcolor = 0
start = time()

USB1 = cv2.VideoCapture(18) 
USB1.set(cv2.CAP_PROP_FRAME_WIDTH, width)
USB1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
if not USB1.isOpened():
    print("Error opening video stream or file USB1")
    exit()

USB2 = cv2.VideoCapture(16) 
USB2.set(cv2.CAP_PROP_FRAME_WIDTH, width)
USB2.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
if not USB2.isOpened():
    print("Error opening video stream or file USB2")
    exit()

picam1 = Picamera2(1)
if not picam1:
    print("falied to open the PiCamera1")
    exit()
picam1.configure(picam1.create_still_configuration({"size": (width, height)}))
picam2 = Picamera2(0)
if not picam2:
    print("falied to open the PiCamera0")
    exit()
picam2.configure(picam2.create_still_configuration({"size": (width, height)}))

picam1.start()
picam2.start()
i = 0
imageConnector = ImageConnector(width,height)
print('setup gotowy')
while True:
    #print('reading frame1')
    ret, frame1 = USB1.read()
    #print('reading frame2')
    ret, frame2 = USB2.read()
    #print('reading frame3')
    frame3 = picam1.capture_array()
    #print('reading frame4')
    frame4 = picam2.capture_array()
    #print('reading frame5')
    frames = [frame1, frame2, frame3, frame4]
    
    #print('Usb type: ', frame1.dtype)
    #print('rpi type: ', frame3.dtype)
    
    #if frame1 is None:
    #    print('usb1 null')
    #if frame2 is None:
    #    print('usb2 null')
    #if frame3 is None:
    #    print('pi1 null')
    #if frame4 is None:
    #    print('pi0 null')
                        
    # cv2.imshow('usb1', frame1)
    # cv2.imshow('usb2', frame2)
    # cv2.imshow('pi1', frame3)
    # cv2.imshow('pi0', frame4)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    if imageConnector.setImages(frames): 
        imageConnector.connectImagesSquare(2)
        connectedImage = imageConnector.getConnectedImage()
    
    
        #cv2.imshow('connected', connectedImage)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    
        #print(connectedImage.dtype)   # Should return CV_8U
        #print(connectedImage.shape)
	
    #frame = np.zeros((height, width, 3), np.uint8)

    # create a rectangle
    # color = colors[curcolor]
    # curcolor += 1
    # curcolor %= len(colors)
    # for y in range(0, int(frame.shape[0] / 2)):
        # for x in range(0, int(frame.shape[1] / 2)):
            # frame[y][x] = color

        out.write(connectedImage)
        print("%s frame written to the server" % datetime.now())
    else:
        print("Frame skipped")
    # now = time()
    # diff = (1 / fps) - now - start
    # if diff > 0:
        # #sleep(diff)
    # start = now
