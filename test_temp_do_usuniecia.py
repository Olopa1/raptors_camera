import cv2
import numpy as np
from picamera2 import Picamera2

# Inicjalizacja Picamera2
camera_index = 1

picam2 = Picamera2(camera_index)
picam2.configure(picam2.create_still_configuration())

# Rozpoczynamy podgląd obrazu
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

# Zakończenie działania kamery i zamknięcie okna OpenCV
picam2.stop()
cv2.destroyAllWindows()
