import cv2
import numpy
import pyvirtualcam
import threading

class VirtualStreamHandler:
    def __init__(self,camWidth:int,camHeight:int,fps:int):
        self.frame = None
        self.width = camWidth
        self.height = camHeight
        self.cam = pyvirtualcam.Camera(width=camWidth,height=camHeight,fps=fps)
        self.frames = []
        self.runFrames = threading.Thread(target=self.__runVirtualCam,daemon=True)
        self.camIsRunnning = False

    def startVirtualCamThread(self):
        self.camIsRunnning = True
        self.runFrames.start()

    def stopVirtualCamThread(self):
        self.camIsRunnning=False
        self.runFrames.join()

    def __runVirtualCam(self):
        while self.camIsRunnning: 
            #print(self.frames)
            if self.frames:
                currentFrame = self.frames.pop(0)
                self.cam.send(currentFrame)
                self.cam.sleep_until_next_frame()   
            else:
                print("Waiting for frames")
    
    def insertFrame(self,frame):
        self.frames.append(frame)

    def getCameraDeviceInfo(self):
        return self.cam.device
    
    def getFramesSent(self):
        return self.cam.frames_sent
    
    

