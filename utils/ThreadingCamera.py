import numpy as np
import time
from picamera2 import Picamera2
from threading import Thread
import cv2

class cameraInputThreading(Thread):

    def __init__(self,cameraId: int,camerasResolution: tuple):
        super().__init__()
        self.cameraId = cameraId
        tempCameraResSize = (camerasResolution[0], camerasResolution[1], 3)
        #print(f"Width: {tempCameraResSize[1]}, Height: {tempCameraResSize[0]}")
        self.frame = np.zeros(tempCameraResSize, dtype='uint8')
        self.frameSize = camerasResolution
        self.cam = None
        self.camRealesed = False
        self.reset = False
        self.loaded = False
        self._fps = 0
        
        self._prevFrameTimeStamp = time.time_ns()
        self._secondTimer = 0
        self._framesCount = 0

    def initCam(self):
        if self.reset: 
            self.cam.stop()
        if not self.loadCamera():
            raise Exception("Cannot open camera")

    def loadCamera(self) -> bool:
        self.cam = Picamera2(self.cameraId)
        if not self.cam:
            #print("falied to open camera")
            return False
        self.cam.configure(self.cam.create_video_configuration({"size": (self.frameSize[1], self.frameSize[0])}))
        self.cam.start()
        print(f"Camera sterted with properties: {self.cam.camera_properties}")
        return True 
    
    def unloadCamera(self):
        if self.cam:
            pass

    def isFrameLoaded(self) -> bool:
        return self.loaded

    def getFrame(self) -> np.ndarray:
        return self.frame
    
    def _countFrames(self):
        frameStart = time.time_ns()
        self._secondTimer += frameStart - self._prevFrameTimeStamp
        self._prevFrameTimeStamp = frameStart
        self._framesCount += 1
        if self._secondTimer >= 10**9:
            self._fps = self._framesCount
            self._framesCount = self._secondTimer = 0

    def run(self) -> None:
        try:
            missedFrames = 0

            self.initCam()
            print(f"Camera with id {self.cameraId} loaded\n")
            while not self.camRealesed:
                #self.frame = self.cam.capture_array()
                self._countFrames()
                frameRaw = self.cam.capture_array()
                textWithBorder(frame=frameRaw,text=f"FPS before stream: {self._fps}")
                if frameRaw is None:
                    missedFrames += 1
                else: 
                    missedFrames = 0
                    time.sleep(0.01)
 
                #print(f"Camera id: {self.cameraId}Frame size: {frameRaw.shape}")
                if frameRaw.shape[2] == 4:
                    frameRaw = frameRaw[:,:,:3]

                self.frame = frameRaw
                #print(f"Frame type: {self.frame.dtype}")
                         
        except Exception as e:
            print("Something went wrong")
            print(e)
            exit()

def loadCameras(camerasList: list) -> list:
    #cameraList must be tuple of camera id and camera resolution that is another tuple in format (height, width)
    #for example: [(0,(1280,720)),(1,(1280,720))]
    cameras = []
    for camera in camerasList:
        c = cameraInputThreading(camera[0],camera[1])
        c.daemon = True
        c.start()
        cameras.append(c)
    return cameras

def textWithBorder(frame, text = "", pos = (0,0), textColor = (0,0,0), borderColor = (128,128,128), fontSize = 1):
  _, h = cv2.getTextSize(text,cv2.FONT_HERSHEY_COMPLEX,fontSize,6)[0]
  cv2.putText(frame,text,(pos[0],pos[1]+h),cv2.FONT_HERSHEY_COMPLEX,fontSize,borderColor,3)
  cv2.putText(frame,text,(pos[0],pos[1]+h),cv2.FONT_HERSHEY_COMPLEX,fontSize,textColor,1)

