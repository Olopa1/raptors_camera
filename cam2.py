import cv2

# Create a VideoCapture object and open the camera (try index 0 if 4 doesn't work)

i = -1
#i=40
while i < 39:
    i+=1
    cap = cv2.VideoCapture(i)  # Index 0 for default camera
    if not cap.isOpened():
        continue
    ret, frame = cap.read()
    if ret:
        print(f'#### video port {i} is working #####')
        cap.release()
cap = cv2.VideoCapture(8)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Check if the camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")
    exit()

i = 7  # Counter for image naming

# Read until video is completed
while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        # Display the resulting frame
        cv2.imshow('Frame', frame)

        # Press 'q' on the keyboard to exit the loop
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

        # Press 'm' to capture and save the current frame
        if cv2.waitKey(25) & 0xFF == ord('m'):
            # Save the captured frame as an image
            filename = f'/home/raptors/Desktop/wojtek/Data_img/test_{i}.png'
            cv2.imwrite(filename, frame)
            print(f"Photo taken and saved: {filename}")
            i += 1

    else:
        break

# When everything is done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
