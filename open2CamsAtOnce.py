import cv2

# Open the camera (0 is usually the default camera on Raspberry Pi)
cap1 = cv2.VideoCapture(0, cv2.CAP_V4L2)
#cap.set(cv2.CAP_PROP_FPS, 1)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

if not cap1.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    #cap.set(cv2.CAP_PROP_FPS, 25)
    ret, frame = cap1.read()
    fps_amount = cap1.get(cv2.CAP_PROP_FPS)
    print("Liczba fps: ", fps_amount)
    if not ret:
        print("Error: Could not read frame.")
        break
    cv2.imshow("stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
#1920x1080 5fps
#640x480 25fps
#l
