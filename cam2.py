import cv2

cap = cv2.VideoCapture(2, cv2.CAP_V4L2)  # Index 0 for default camera
print('is working')
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
cap.set(cv2.CAP_PROP_FPS, 30)
# Check if the camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

i = 0  # Counter for image naming

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #qframe = cv2.flip(cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE),1)
    fps_amount = cap.get(cv2.CAP_PROP_FPS)
    print("Liczba fps: ", fps_amount)
    if ret:
        # Display the resulting frame
        
        cv2.imshow('Frame', frame)

        # Press 'q' on the keyboard to exit the loop
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        # Press 'm' to capture and save the current frame
        if cv2.waitKey(25) & 0xFF == ord('m'):
            # Save the captured frame as an image
            filename = f'/home/raptors/Desktop/wojtek/Calibration/USB3_{i}.png'
            result = cv2.imwrite(filename, frame)
            print(result,' i=',i)
            print(f"Photo taken and saved: {filename}")
            i += 1

    else:
        break

# When everything is done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
