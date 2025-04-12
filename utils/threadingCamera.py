from numpy import ndarray
import time
from picamera2 import Picamera2
from threading import Thread
import cv2

class cameraInputThreading(Thread):

    def __init__(self,cameraId: int,camerasResolution: tuple):
        super().__init__()
        self.cameraId = cameraId
        self.frame = ndarray(camerasResolution)
        self.frameSize = camerasResolution
        self.cam = None
        self.camRealesed = False
        self.reset = False
        self.loaded = False

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
        self.cam.configure(self.cam.create_still_configuration({"size": (self.frameSize[0], self.frameSize[1])}))
        return True 
    
    def unloadCamera(self):
        if self.cam:

    def isFrameLoaded(self) -> bool:
        return self.loaded

    def getFrame(self) -> ndarray:
        return self.frame
    
    def run(self) -> None:
        try:
            missedFrames = 0
            self.initCam()
            print(f"Camera with id {self.cameraId} loaded\n")
            while not self.camRealesed:
                self.frame = self.cam.capture_array()
                if not self.frame:
                    missedFrames += 1
                else: 
                    missedFrames = 0
                    time.sleep(0.01)
                if missedFrames == 50:
                    print("To much missed frames exiting loop")
                    break
                          
        except:
            print("Something went wrong")
            exit()

def loadCameras(camerasList: list) -> list:
    cameras = []
    for camera in camerasList:
        c = cameraInputThreading(camera[0],camera[1])
        c.daemon = True
        c.start()
        cameras.append
    return cameras

