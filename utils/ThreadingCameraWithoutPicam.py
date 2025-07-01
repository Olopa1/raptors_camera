import numpy as np
import time
from threading import Thread
import cv2


class cameraInputThreading(Thread):

    def __init__(self, cameraId: int, camerasResolution: tuple):
        super().__init__()
        self.cameraId = cameraId
        tempCameraResSize = (camerasResolution[0], camerasResolution[1], 3)
        # print(f"Width: {tempCameraResSize[1]}, Height: {tempCameraResSize[0]}")
        self.frame = np.ndarray(tempCameraResSize, dtype='uint8')
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
        self.cam = cv2.VideoCapture(0)
        if not self.cam:
            # print("falied to open camera")
            return False
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.frameSize[0])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.frameSize[1])

        # print(f"Camera sterted with properties: {self.cam.camera_properties}")
        return True

    def unloadCamera(self):
        if self.cam:
            pass

    def isFrameLoaded(self) -> bool:
        return self.loaded

    def getFrame(self) -> np.ndarray:
        return self.frame

    def run(self) -> None:
        try:
            missedFrames = 0
            self.initCam()
            print(f"Camera with id {self.cameraId} loaded\n")
            while not self.camRealesed:
                # self.frame = self.cam.capture_array()
                ret, frameRaw = self.cam.read()
                if not ret:
                    raise Exception("Could not read frame from camera")

                # Convert frame to RGB
                frameRaw = cv2.cvtColor(frameRaw, cv2.COLOR_BGR2RGB)
                # frameRaw = self.cam.capture_array()
                print(f"Camera id: {self.cameraId}Frame size: {frameRaw.shape}")
                if frameRaw.shape[:2] != (self.frameSize[0], self.frameSize[1]):
                    if frameRaw.shape[2] == 4:
                        frameRaw = frameRaw[:, :, :3]

                    self.frame = cv2.resize(frameRaw, (self.frameSize[1], self.frameSize[0]))
                    # print()
                else:
                    self.frame = frameRaw
                # print(f"Frame type: {self.frame.dtype}")
                if self.frame is None or np.any(self.frame):
                    missedFrames += 1
                else:
                    missedFrames = 0
                    time.sleep(0.01)
                # if missedFrames == 1000:
                #    print("To much missed frames exiting loop")
                #    break

        except Exception as e:
            print("Something went wrong")
            print(e)
            exit()


def loadCameras(camerasList: list) -> list:
    # cameraList must be tuple of camera id and camera resolution that is another tuple in format (height, width)
    # for example: [(0,(1280,720)),(1,(1280,720))]
    cameras = []
    for camera in camerasList:
        c = cameraInputThreading(camera[0], camera[1])
        c.daemon = True
        c.start()
        cameras.append(c)
    return cameras

