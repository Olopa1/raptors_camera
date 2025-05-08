import numpy as np
from typing import Optional
import math

class ImageConnectorBase:
    
    def __init__(self,imageWidth,imageHeight):
        self.singleImageWidth = imageWidth
        self.singleImageHeight = imageHeight
        self.images = []
        self.lastFrame = None
        self._initFrame()

    def _initFrame(self):
        """This method must be overriden with implementation of frame init"""
        pass
    
    def connectImages(self) -> bool:
        """This method must be overriden with your image connection implementation"""
        pass

    def setImages(self,images:list)->bool:
        '''Pass the list of frames to connect it might be as many as you want'''
        self.images.clear()
        for i in images:
            if i is None:
                return False
            self.images.append(i)
        return True
    
    def getConnectedImage(self) -> Optional[np.ndarray]:
        '''returns last connected image or none if there was none prevoisly'''
        return self.lastFrame
