import warnings
import cv2
import time
# Suppress specific OpenCV warnings (like OpenCV deprecation warnings)
warnings.filterwarnings("ignore", category=UserWarning, module='cv2')

# Open the camera (0 is usually the default camera on Raspberry Pi)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Capture a frame from the camera
for i in range(0,5):
    ret, frame = cap.read()

    if ret:
    # Save the captured frame as an image
        string = '/home/hackathon/Desktop/wojtek/Data_img1/board4' + str(i)+'.png'
        cv2.imwrite(string, frame)
        print("Photo taken and saved!", i)
    else:
        print("Error: Could not capture image.")
    time.sleep(3)

# Release the camera
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
