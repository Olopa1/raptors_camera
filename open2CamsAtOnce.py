import cv2
import numpy as np
from picamera2 import Picamera2
# Open the camera (0 is usually the default camera on Raspberry Pi)
cap1 = cv2.VideoCapture(8, cv2.CAP_V4L2)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap1.isOpened():
	print("Error: 1 Could not open the USB Camera.")
	exit()


while True:
    ret, frame = cap1.read()
    fps_amount = cap1.get(cv2.CAP_PROP_FPS)
    print("Liczba fps: ", fps_amount)
    if not ret:
        print("Error: Could not read frame.")
        break
    cv2.imshow("stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()

picam2 = Picamera2(0)
if not picam2:
    print("falied to open the PiCamera")
    exit()
picam2.configure(picam2.create_still_configuration())

picam2.start()
while True:
    # Pobranie obrazu z kamery
    image = picam2.capture_array()

    # Przetwarzanie obrazu w OpenCV (np. konwersja na skalę szarości)
    toCvFormat = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Wyświetlanie obrazu w oknie
    cv2.imshow("Camera", toCvFormat)

    # Jeśli naciśniesz 'q', program zakończy działanie
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
#1920x1080 5fps
#640x480 25fps
