import numpy
from typing import Optional
import math

class ImageConnector:
    def __init__(self,imageWidth,imageHeight):
        self.singleImageWidth = imageWidth
        self.singleImageHeight = imageHeight
        self.images = []
        self.lastFrame = None

    def setImages(self,images:list)->bool:
        '''Pass the list of frames to connect it might be as many as you want'''
        self.images.clear()
        for i in images:
            if i is None:
                return False
            self.images.append(i)
        return True

    def connectImagesWide(self) -> bool:
        '''Connect passed images into one wide image. It might return false if no image were passed in setImage before'''
        if not self.images:
            return False
        tempNewImageConnected = numpy.zeros((self.singleImageHeight,self.singleImageWidth*len(self.images),3), dtype=numpy.uint8)
        for i in range(len(self.images)):
            widthOffset = self.singleImageWidth * i
            tempNewImageConnected[:,widthOffset:self.singleImageWidth + widthOffset,:] = self.images[i]
        self.lastFrame = tempNewImageConnected
        return True

    def connectImagesSquare(self,framesInOneRow:int) -> bool:
        if not self.images:
            return False

        cols = framesInOneRow
        rows = math.ceil(len(self.images) / framesInOneRow)
        tempNewImageConnected = numpy.zeros((self.singleImageHeight*rows,self.singleImageWidth*cols,3), dtype=numpy.uint8)
        heightOffset = -self.singleImageHeight
        for i in range(len(self.images)):
            widthOffset = self.singleImageWidth * (i%framesInOneRow)
            heightOffset += self.singleImageHeight if widthOffset == 0 else 0
            tempNewImageConnected[heightOffset:self.singleImageHeight + heightOffset,widthOffset:self.singleImageWidth + widthOffset,:] = self.images[i]
        self.lastFrame = tempNewImageConnected
        return True

    def getConnectedImage(self) -> Optional[numpy.ndarray]:
        '''returns last connected image or none if there was none prevoisly'''
        return self.lastFrame
