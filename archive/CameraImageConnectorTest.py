import numpy
import cv2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.ImageConnectorsCollection import ImageConnectorSquare, ImageConnectorPanoramic, ImageConnectorHorizontalSplit, ImageConnectorVerticalSplit

image1 = cv2.imread("../archive/Calibration/USB1_0.png")
image2 = cv2.imread("../archive/Calibration/USB1_1.png")
image3 = cv2.imread("../archive/Calibration/USB1_2.png")
image4 = cv2.imread("../archive/Calibration/USB1_3.png")

width = image1.shape[1]
height = image1.shape[0]
print(f"width:{width} height:{height}")
imageConnector = ImageConnectorPanoramic(width,height)
imageConnector.setImages({"front":image1, "back":image2, "left":image3, "right":image4})
imageConnector.connectImages()
imageConnector.setFpsInfo({"front":11, "back":12, "left":13, "right":14}, 15)
connectedImage = imageConnector.getConnectedImage()
cv2.imwrite("../archive/Calibration/connected_image_panoramic.png",connectedImage)

imageConnector = ImageConnectorSquare(width,height)
imageConnector.setImages({"front":image1, "back":image2, "left":image3, "right":image4})
imageConnector.connectImages()
imageConnector.setFpsInfo({"front":11, "back":12, "left":13, "right":14}, 15)
connectedImage = imageConnector.getConnectedImage()
cv2.imwrite("../archive/Calibration/connected_image_square.png",connectedImage)

imageConnector = ImageConnectorVerticalSplit(width,height)
imageConnector.setImages({"front":image1, "back":image2, "left":image3, "right":image4})
imageConnector.connectImages()
imageConnector.setFpsInfo({"front":11, "back":12, "left":13, "right":14}, 15)
connectedImage = imageConnector.getConnectedImage()
cv2.imwrite("../archive/Calibration/connected_image_vertical.png",connectedImage)

imageConnector = ImageConnectorHorizontalSplit(width,height)
imageConnector.setImages({"front":image1, "back":image2, "left":image3, "right":image4})
imageConnector.connectImages()
imageConnector.setFpsInfo({"front":11, "back":12, "left":13, "right":14}, 15)
connectedImage = imageConnector.getConnectedImage()
cv2.imwrite("../archive/Calibration/connected_image_horizontal.png",connectedImage)
