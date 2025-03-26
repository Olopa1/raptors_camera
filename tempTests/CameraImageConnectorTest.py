import numpy
import cv2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.CameraImageConnector import ImageConnector

image1 = cv2.imread("../images/Calibration/USB1_0.png")
image2 = cv2.imread("../images/Calibration/USB1_1.png")
image3 = cv2.imread("../images/Calibration/USB1_2.png")
image4 = cv2.imread("../images/Calibration/USB1_3.png")

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
