import cv2
import warnings
warnings.filterwarnings("ignore") 
# Open the camera (0 is usually the default camera on Raspberry Pi)

for i in range(19,38):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print("£££££££££££££££££££." , i)

for i in range(0,5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print("£££££££££££££££££££." , i)
# Capture a frame from the camera
ret, frame = cap.read()

if ret:
    # Save the captured frame as an image
    cv2.imwrite('photo_opencv.jpg', frame)
    print("Photo taken and saved!")
else:
    print("Error: Could not capture image.")

# Release the camera
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
