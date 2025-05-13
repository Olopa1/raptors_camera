from time import sleep

import numpy as np
import time
from picamera2 import Picamera2
from threading import Thread, Event
import cv2

class cameraInputThreading(Thread):

    def __init__(self,camMetaData: dict):
        super().__init__()
        self.cameraId = camMetaData["camId"]
        self.label = camMetaData["camLabel"]
        tempCameraResSize = (camMetaData["camWidth"], camMetaData["camHeight"], 3)
        self.frame = np.zeros(tempCameraResSize, dtype='uint8')
        print(self.frame.shape)
        self.frameSize = (camMetaData["camWidth"], camMetaData["camHeight"])
        self.cam = None
        self.camRealesed = False
        self.reset = False
        self.loaded = False
        self.fps = 0
        self.frameReady = Event()
        self.frameRaw = np.zeros(tempCameraResSize, dtype='uint8')
        
        self._prevFrameTimeStamp = time.time_ns()
        self._secondTimer = 0
        self._framesCount = 0

    def initCam(self):
        if self.reset: 
            self.cam.stop()
            self.reset = False
        if not self.loadCamera():
            raise Exception("Cannot open camera")

    def loadCamera(self) -> bool:
        self.cam = Picamera2(self.cameraId)
        if not self.cam:
            #print("falied to open camera")
            return False
        self.cam.configure(self.cam.create_video_configuration({"size": (self.frameSize[1], self.frameSize[0]), "format": "RGB888"}))
        self.cam.start()
        #print(f"Camera sterted with properties: {self.cam.camera_properties}")
        self.loaded = True
        return True 
    
    def unloadCamera(self):
        if self.cam:
            pass

    def isFrameLoaded(self) -> bool:
        return self.loaded

    def getFrame(self) -> tuple[str, np.ndarray]:
        return self.label, self.frame
    
    def _countFrames(self):
        frameStart = time.time_ns()
        self._secondTimer += frameStart - self._prevFrameTimeStamp
        self._prevFrameTimeStamp = frameStart
        self._framesCount += 1
        if self._secondTimer >= 10**9:
            self.fps = self._framesCount
            self._framesCount = self._secondTimer = 0

    def signalFun(self, job):
        try:
            self.frameRaw = self.cam.wait(job)
        except Exception as e:
            print("Exception in signal function:", e)
        finally:
            self.frameReady.set()

    def run(self) -> None:
        try:
            missedFrames = 0
            aliveCount = 0

            self.initCam()
            print(f"Camera with id {self.cameraId} loaded\n")
            while not self.camRealesed:
                if not self.loaded:
                    self.initCam()
                    sleep(1)
                    continue

                self.alive = False
                self.frameReady.clear()
                job = self.cam.capture_array(wait=False, signal_function=self.signalFun)

                self._countFrames()

                if self.frameReady.wait(timeout=2):  # wait max 2 seconds
                    pass
                else:
                    print("Camera not responding! Possibly disconnected.")
                    self.loaded = False
                    self.initCam()
                    continue

                if self.frameRaw is None:
                    missedFrames += 1
                else: 
                    missedFrames = 0
                    time.sleep(0.01)
                if missedFrames >= 300:
                    print("300frames missed\n")
                    self.reset = True
                    self.initCam()
                print(f"Camera id: {self.cameraId}Frame size: {self.frameRaw.shape}")

                self.frame = self.frameRaw
                #print(f"Frame type: {self.frame.dtype}")
        
        except Exception as e:
            print("Something went wrong")
            print(e)
            exit()

def loadCameras(camerasDict: dict) -> list:
    #cameraList must be tuple of camera id and camera resolution that is another tuple in format (height, width)
    #for example: [(0,(1280,720)),(1,(1280,720))]
    cameras = []
    cameraParamDict = {"camId": 0, "camLabel": "", "camWidth": 0, "camHeight": 0}
    for camera in camerasDict.keys():
        cameraParamDict["camId"] = camerasDict[camera][0]
        cameraParamDict["camWidth"] = camerasDict[camera][1][0]
        cameraParamDict["camHeight"] = camerasDict[camera][1][1]
        cameraParamDict["camLabel"] = camera
        
        c = cameraInputThreading(cameraParamDict)
        c.daemon = True
        c.start()
        cameras.append(c)
    return cameras
