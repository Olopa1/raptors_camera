#ten kod wysyla stream do wifi po webrtc!!!
import asyncio
import ssl
import uuid
import logging
import argparse
import json
import pathlib
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer, MediaRelay, MediaRecorder
from av import VideoFrame
from time import time_ns
import sys
import os
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.CameraImageConnector import ImageConnector
from utils.ThreadingCamera import loadCameras,textWithBorder

fps = 120
width = 640
height = 480

logger = logging.getLogger("pc")
pcs = set()
relay = MediaRelay()

ROOT = pathlib.Path(__file__).parent  # <-- Path to find index.html

class CameraStreamTrack(VideoStreamTrack):
    """
    A video stream track that returns frames from a camera (using OpenCV).
    """

    isInitialized = False
    camerasLoaded = None
    cameras = None

    def __init__(self):
        super().__init__()

        self.imageConnector = ImageConnector(width, height)
        self.frames = []

        self._fps = 0
        
        self._prevFrameTimeStamp = time_ns()
        self._secondTimer = 0
        self._framesCount = 0



        if CameraStreamTrack.isInitialized is False:
            self.setup()
            CameraStreamTrack.isInitialized = True

    async def recv(self):
        try:
            
            tempFrameStart = time_ns()
            # sleep to simulate fps
            await asyncio.sleep(1/fps)
            self._countFrames()
            # print("recv() called")
            pts, time_base = await self.next_timestamp()

            if CameraStreamTrack.camerasLoaded is None:
                raise Exception("Cameras not yet loaded")

            # Get frames from async threads and connect them
            frames = [frame.getFrame() for frame in CameraStreamTrack.camerasLoaded]
            self.imageConnector.setImages(frames)
            if self.imageConnector.connectImagesSquare(2):
                image = self.imageConnector.getConnectedImage()
                if image is None:
                    raise Exception("Error getting connected image")
            
            else:
                raise Exception("Error connecting frames")
            #myText = f"Nanos of fram connecting: {(tempFrameStop - tempFrameStart)/10**9}"
            textWithBorder(frame=image,text=f"FPS after stream: {self._fps}", pos=(0,200))
        except Exception as e:
            print("Exception in recv():", e)
            image = np.zeros((height, width, 3), dtype=np.uint8)  # black frame

        # Create VideoFrame
        video_frame = VideoFrame.from_ndarray(image, format="rgb24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        tempFrameStop = time_ns()
        print(f"Time for method to run: {(tempFrameStop - tempFrameStart)/10**9}")
        return video_frame

    def setup(self) -> None:
        """
        Initializes cameras.
        """

        CameraStreamTrack.cameras = {"Camera1": (0, (height,width)), "Camera2": (1,(height,width)), "Camera3": (2,(height,width)), "Camera4": (3,(height,width))}
        # print("init")
        print(CameraStreamTrack.cameras.values())

        CameraStreamTrack.camerasLoaded = loadCameras(self.cameras.values())
        print(CameraStreamTrack.camerasLoaded)
        if not CameraStreamTrack.camerasLoaded:
            print(CameraStreamTrack.camerasLoaded)
            print("Error loading cameras")
            exit()

        print('setup ready')

    def _countFrames(self):
        frameStart = time_ns()
        self._secondTimer += frameStart - self._prevFrameTimeStamp
        self._prevFrameTimeStamp = frameStart
        self._framesCount += 1
        if self._secondTimer >= 10**9:
            self._fps = self._framesCount
            self._framesCount = self._secondTimer = 0


async def offer(request):
    params = await request.json()
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    # <- ADD STUN SERVER!
    pc = RTCPeerConnection(configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

    pcs.add(pc)
    ### 
    #params = await request.json()
    #offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()
    pcs.add(pc)

    # Add our camera stream
    camera = CameraStreamTrack()
    sender = pc.addTrack(camera)

    try:
        params = sender.getParameters()
    
        if not params.encodings:
        # jeśli brak encodings, trzeba dodać domyślny encoding
            params.encodings = [{}]

    # Teraz możesz ustawić bitrate
        params.encodings[0]["maxBitrate"] = 1_000  # np. 2 Mbps

        await sender.setParameters(params)

    except Exception as e:
        print("Błąd podczas ustawiania maxBitrate:", e)

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

async def javascript(request):
    content = open(os.path.join(ROOT, "client.js"), "r").read()
    return web.Response(content_type="application/javascript", text=content)


async def on_shutdown(app):
    # Cleanup
    coros = [pc.close() for pc in pcs]
    await asyncio.gather(*coros)
    pcs.clear()


app = web.Application()
app.router.add_get("/", index)        # <-- serve index.html at /
app.router.add_get("/client.js", javascript)
app.router.add_post("/offer", offer)
app.on_shutdown.append(on_shutdown)

web.run_app(app, host='0.0.0.0', port=8089)
