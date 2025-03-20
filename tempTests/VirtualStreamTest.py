import colorsys
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.VirtualStreamCam import VirtualStreamHandler

virtualCam = VirtualStreamHandler(1280,720,20)
virtualCam.getCameraDeviceInfo()
virtualCam.startVirtualCamThread()

frame = np.zeros((virtualCam.height, virtualCam.width, 3), np.uint8) 
while True:
    h, s, v = (virtualCam.getFramesSent() % 100) / 100, 1.0, 1.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    frame[:] = (r * 255, g * 255, b * 255)
    virtualCam.insertFrame(frame)  

