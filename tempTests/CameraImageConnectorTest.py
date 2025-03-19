from utils.CameraImageConnector import ImageConnector
import numpy
import cv2

image1 = cv2.imread("../images/calibration/USB1_0.png")
image2 = cv2.imread("../images/calibration/USB1_1.png")
image3 = cv2.imread("../images/calibration/USB1_2.png")
image4 = cv2.imread("../images/calibration/USB1_3.png")

width = image1.shape[1]
height = image1.shape[0]
print(f"width:{width} height:{height}")
imageConnector = ImageConnector(width,height)
imageConnector.setImages([image1,image2,image3,image4])
imageConnector.connectImagesSquare(2)
connectedImage = imageConnector.getConnectedImage()
cv2.imwrite("../images/calibration/connected_image_square.png",connectedImage)
imageConnector.connectImagesWide()
connectedImage = imageConnector.getConnectedImage()
cv2.imwrite("../images/calibration/connected_image.png",connectedImage)
