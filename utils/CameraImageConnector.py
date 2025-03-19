import numpy
from typing import Optional

class ImageConnector:
    def __init__(self,imageWidth,imageHeight):
        self.singleImageWidth = imageWidth
        self.singleImageHeight = imageHeight
        self.images = []
        self.lastFrame = None

    def setImages(self,images:list):
        self.images.clear()
        for i in images:
            self.images.append(i)

    def connectImages(self) -> bool:
        if not self.images:
            return False
        tempNewImageConnected = numpy.zeros((self.singleImageHeight,self.singleImageWidth*len(self.images),3))
        for i in range(len(self.images)):
            widthOffset = self.singleImageWidth * i
            tempNewImageConnected[:,widthOffset:self.singleImageWidth + widthOffset,:] = self.images[i]
        self.lastFrame = tempNewImageConnected
        return True

    def getConnectedImage(self) -> Optional[numpy.ndarray]:
        return self.lastFrame
