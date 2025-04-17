#ten kod wysyla stream do wifi po webrtc!!!
import asyncio
import cv2
import pathlib
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer
from av import VideoFrame
from datetime import datetime
from time import sleep, time
import sys
import os
import cv2
import numpy as np
from picamera2 import Picamera2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.CameraImageConnector import ImageConnector
from utils.ThreadingCamera import loadCameras

fps = 15
width = 1280
height = 720

pcs = set()
ROOT = pathlib.Path(__file__).parent  # <-- Path to find index.html

class CameraStreamTrack(VideoStreamTrack):
    """
    A video stream track that returns frames from a camera (using OpenCV).
    """

    isInitialized = False

    def __init__(self):
        super().__init__()

        if CameraStreamTrack.isInitialized is False:
            self.imageConnector = None
            self.frames = []
            self.camerasLoaded = None
            self.cameras = None
            self.setup()
            CameraStreamTrack.isInitialized = True

    async def recv(self):
        await asyncio.sleep(1 / 15) # 15 fps
        #print("recv() called")
        pts, time_base = await self.next_timestamp()

        # Get frames from async threads and connect them
        frames = [frame.getFrame() for frame in self.camerasLoaded]
        self.imageConnector.setImages(frames)
        if self.imageConnector.connectImagesSquare(2):
            image = self.imageConnector.getConnectedImage()
            if image is None:
                print("Error getting connected image")
                image = np.zeros((height, width, 3), dtype=np.uint8)  # black frame

        else:
            print("Error connecting frames")
            print("Frame skipped")
            image = np.zeros((height, width, 3), dtype=np.uint8)  # black frame

        # Create VideoFrame
        video_frame = VideoFrame.from_ndarray(image, format="rgb24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame

    def setup(self) -> None:
        """
        Initializes cameras.
        :return:
        """
        self.cameras = {"Camera1": (0, (height,width)), "Camera2": (1,(height,width)), "Camera3": (2,(height,width)), "Camera4": (3,(height,width))}
        print("init")
        print(self.cameras.values())

        self.camerasLoaded = loadCameras(self.cameras.values())
        self.frames = []
        self.imageConnector = ImageConnector(width,height)
        print(self.camerasLoaded)
        if not self.camerasLoaded:
            print(self.camerasLoaded)
            print("Error loading cameras")
            exit()

        print('setup ready')


async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    # <- ADD STUN SERVER!
    pc = RTCPeerConnection(configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    pcs.add(pc)
    ### 
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    # Add our camera stream
    camera = CameraStreamTrack()
    pc.addTrack(camera)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.json_response(
        {
            "sdp": pc.localDescription.sdp,
            "type": pc.localDescription.type
        }
    )

async def index(request):
    content = (ROOT / "index.html").read_text()
    return web.Response(content_type="text/html", text=content)

async def on_shutdown(app):
    # Cleanup
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


app = web.Application()
app.router.add_get("/", index)        # <-- serve index.html at /
app.router.add_post("/offer", offer)
app.on_shutdown.append(on_shutdown)

web.run_app(app, host='0.0.0.0', port=8089)
