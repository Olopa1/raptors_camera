import numpy as np
from typing import Optional
import math

class ImageConnectorBase:
    
    def __init__(self,imageWidth,imageHeight):
        self.singleImageWidth = imageWidth
        self.singleImageHeight = imageHeight
        self.images = {}
        self.lastFrame = None
        self._initFrame()

    def _initFrame(self):
        """This method must be overriden with implementation of frame init"""
        pass
    
    def connectImages(self) -> bool:
        """This method must be overriden with your image connection implementation"""
        pass

    def setImages(self,frames:dict)->bool:
        '''Pass the list of frames to connect it might be as many as you want'''
        self.images = frames
        return True
    
    def getConnectedImage(self) -> Optional[np.ndarray]:
        '''returns last connected image or none if there was none prevoisly'''
        return self.lastFrame
    

class ImageConnectorPanoramic(ImageConnectorBase):
    
    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)
    
    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight,self.singleImageWidth * 4,3),dtype=np.uint8)

    def connectImages(self):
        widthOffset = self.singleImageWidth
        self.lastFrame[:,:widthOffset,:] = self.images["left"] if self.images["left"] is not None else 0
        self.lastFrame[:,widthOffset:widthOffset * 2,:] = self.images["front"] if self.images["front"] is not None else 0
        self.lastFrame[:,widthOffset*2:widthOffset*3,:] = self.images["right"] if self.images["right"] is not None else 0
        self.lastFrame[:,widthOffset*3:,:] = self.images["back"] if self.images["back"] is not None else 0
        return True


class ImageConnectorSquare(ImageConnectorBase):
    
    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)
    
    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight * 2,self.singleImageWidth * 2,3),dtype=np.uint8)

    def connectImages(self):
        widthOffset = self.singleImageWidth
        heightOffset = self.singleImageHeight

        self.lastFrame[:heightOffset,:widthOffset,:] = self.images["front"] if self.images["front"] is not None else 0
        self.lastFrame[:heightOffset,widthOffset:,:] = self.images["back"] if self.images["back"] is not None else 0
        self.lastFrame[heightOffset:,:widthOffset,:] = self.images["left"] if self.images["left"] is not None else 0
        self.lastFrame[heightOffset:,widthOffset:,:] = self.images["right"] if self.images["right"] is not None else 0
        return True
    