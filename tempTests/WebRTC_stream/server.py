#ten kod wysyla stream do wifi po webrtc!!!
import asyncio
import cv2
import pathlib
from aiohttp import web
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack
from aiortc.contrib.media import MediaBlackhole, MediaPlayer
from av import VideoFrame

pcs = set()
ROOT = pathlib.Path(__file__).parent  # <-- Path to find index.html

class CameraStreamTrack(VideoStreamTrack):
    """
    A video stream track that returns frames from a camera (using OpenCV).
    """
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)  # 0 = default webcam

    async def recv(self):
        #print("recv() called")
        pts, time_base = await self.next_timestamp()

        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Could not read frame from camera")

        # Convert frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create VideoFrame
        video_frame = VideoFrame.from_ndarray(frame, format="rgb24")
        video_frame.pts = pts
        video_frame.time_base = time_base
        return video_frame

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

web.run_app(app, host='0.0.0.0', port=8080)

