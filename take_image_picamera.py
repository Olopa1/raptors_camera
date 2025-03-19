import cv2
import numpy as np
from picamera2 import Picamera2

picam2 = Picamera2(1)
if not picam2:
    print("falied to open the PiCamera")
    exit()
picam2.configure(picam2.create_still_configuration({"size": (1920, 1280)}))
i = 0
picam2.start()
while True:
    # Pobranie obrazu z kamery
    image = picam2.capture_array()

    # Przetwarzanie obrazu w OpenCV (np. konwersja na skalę szarości)
    toCvFormat = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Wyświetlanie obrazu w oknie
    cv2.imshow("Camera", toCvFormat)
    
    # Press 'm' to capture and save the current frame
    if cv2.waitKey(25) & 0xFF == ord('m'):
        # Save the captured frame as an image
        filename = f'/home/raptors/Desktop/wojtek/Calibration/PiCam_solo/PiCamS_{i}.png'
        result = cv2.imwrite(filename, frame)
        
        print(f"Photo taken and saved: {filename}")
        i += 1

    # Jeśli naciśniesz 'q', program zakończy działanie
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
#1920x1080 5fps
#640x480 25fps
