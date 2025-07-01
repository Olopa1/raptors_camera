import cv2

# Initialize the camera (use 0 for default webcam)
cap = cv2.VideoCapture(2)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open video stream or file")
    exit()

# Get the video frame width and height to set the output video size
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create VideoWriter object
# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can also use 'MJPG', 'MP4V', etc.
out = cv2.VideoWriter('read_text.mp4', fourcc, 20.0, (frame_width, frame_height))

print("Recording video. Press 'q' to stop.")

# Loop to capture frames and write to the video file
while cap.isOpened():
    ret, frame = cap.read()
    print(ret)
    print(frame)    
    if ret:
        # Write the frame to the video file
        out.write(frame)

        # Display the frame in a window
        cv2.imshow('Recording Video', frame)

        # Press 'q' to exit the loop and stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #else:
    #    break

# Release the video capture and writer objects
cap.release()
out.release()

# Close all OpenCV windows
cv2.destroyAllWindows()

print("Video recording stopped.")
