import cv2
import threading
import time
import os
import stat

cam1 = 2
cam2 = 5
cap = cv2.VideoCapture(cam2)



# Ścieżka do folderu
photos_dir = 'photos'

# Utwórz folder, jeśli nie istnieje
os.makedirs(photos_dir, exist_ok=True)

# Nadaj uprawnienia do odczytu i zapisu (rwxr-xr-x)
os.chmod(photos_dir, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

latest_frame = None
running = True

def capture_frames():
    global latest_frame, running
    while running:
        ret, frame = cap.read()
        if ret:
            # Skalowanie ramki
            latest_frame = frame #cv2.flip(frame, 1)
        else:
            time.sleep(0.01)

thread = threading.Thread(target=capture_frames, daemon=True)
thread.start()

print("is working")
i = 1

while True:
    if latest_frame is not None:
        scale_x, scale_y = 0.9, 0.9
        frame_2 = cv2.resize(latest_frame, None, fx=scale_x, fy=scale_y, interpolation=cv2.INTER_AREA)
        #reverse
        #frame_2 = cv2.flip(x, 1) 
        cv2.imshow('Obraz z manipulatora', frame_2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        running = False   # zatrzymujemy wątek
        thread.join()     # czekamy na jego zakończenie
        break
    elif key == ord('m') and latest_frame is not None:
        filename = f'science/picture_{i}.png' #/Documents/uczelnia/RAPTORS/project_camera360/calibration
        cv2.imwrite(filename, latest_frame)
        print(f"Photo taken and saved: {filename}")
        i += 1

cap.release()
cv2.destroyAllWindows()
