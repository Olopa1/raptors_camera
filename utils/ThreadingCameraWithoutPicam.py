import numpy as np
import time
from threading import Thread
import cv2


class cameraInputThreading(Thread):

    def __init__(self, cameraId: int, camerasResolution: tuple, videoPath: str, lbl: str):
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
        self.videoPath = videoPath
        self.label = lbl

    def initCam(self):
        if self.reset:
            self.cam.stop()
        if not self.loadCamera(self.videoPath):
            raise Exception("Cannot open camera")

    def loadCamera(self, videoPath: str) -> bool:
        if len(videoPath) == 0:
            self.cam = cv2.VideoCapture(0)
        else:
            self.cam = cv2.VideoCapture(videoPath)
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

    def getFrame(self) -> tuple:
        return self.label, self.frame

    def run(self) -> None:
        try:
            missedFrames = 0
            self.initCam()
            print(f"Video stream loaded from file\n")
            while not self.camRealesed:
                ret, frameRaw = self.cam.read()

                if not ret:
                    print("Restarting video...")
                    self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)  # wracamy na początek pliku
                    continue

                frameRaw = cv2.cvtColor(frameRaw, cv2.COLOR_BGR2RGB)

                if frameRaw.shape[:2] != (self.frameSize[0], self.frameSize[1]):
                    if frameRaw.shape[2] == 4:
                        frameRaw = frameRaw[:, :, :3]
                    self.frame = cv2.resize(frameRaw, (self.frameSize[1], self.frameSize[0]))
                else:
                    self.frame = frameRaw

                if self.frame is None or np.any(self.frame):
                    missedFrames += 1
                else:
                    missedFrames = 0
                    time.sleep(0.01)

        except Exception as e:
            print("Something went wrong")
            print(e)
            exit()


def loadCameras(images: int) -> list:
    # Zamiast kamery, otwieramy plik
    video_path = "C:\\dominik_rzeczy\\programy\\raptors_camera\\static\\videotest.mp4"  # tu podaj swoją ścieżkę do pliku
    cameras = []
    sides = ["front","back","left","right"]
    # CameraStreamTrack.cameras = {"front": (0, (height,width)),
    #                            "back": (1,(height,width)),
    #                            "left": (2,(height,width)),
    #                            "right": (3,(height,width))}
    for i in range(images):
        camera = cameraInputThreading(i, (480,640), video_path, sides[i])
        camera.daemon = True
        camera.start()
        cameras.append(camera)

    #print(cameras)
    return cameras