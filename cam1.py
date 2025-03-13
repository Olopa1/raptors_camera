# importing libraries
import cv2

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(0)
print('is working')
# Check if camera opened successfully
if (cap.isOpened()== False):
    print("Error opening video file")
i=0
# Read until video is completed
while(cap.isOpened()):
    
# Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
    # Display the resulting frame
        cv2.imshow('Frame', frame)
        
    # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
        if 0xFF == ord('m'):
            ret, frame = cap.read()
            if ret:
            # Save the captured frame as an image
                string = '/home/hackathon/Desktop/wojtek/Data_img1/board3' + str(i)+'.png'
                i+=1
                cv2.imwrite(string, frame)
                print("Photo taken and saved!", i)
            else:
                print("Error: Could not capture image.")
# Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()