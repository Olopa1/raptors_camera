from picamera2 import Picamera2
from time import sleep
camera = Picamera2()
camera.start_preview(alpha=192)
sleep(1)
camera.capture('wojo.png')
camera.stop_preview()