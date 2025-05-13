import numpy as np
from typing import Optional

class ImageConnectorBase:
    
    def __init__(self, imageWidth, imageHeight):
        self.singleImageWidth = imageWidth
        self.singleImageHeight = imageHeight
        self.images = {}
        self.lastFrame = None
        self._initFrame()

    def _initFrame(self):
        """This method must be overridden with implementation of frame init"""
        pass
    
    def connectImages(self) -> bool:
        """This method must be overridden with your image connection implementation"""
        pass

    def setImages(self,frames:dict)->bool:
        """Pass the dict of frames to connect. Labels should be: front, back, left, right."""
        self.images = frames
        return True
    
    def getConnectedImage(self) -> Optional[np.ndarray]:
        """returns last connected image or black frame if there was none previously"""
        return self.lastFrame
    

class ImageConnectorPanoramic(ImageConnectorBase):
    """Connector that connects images in a panoramic view"""

    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)
    
    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight,self.singleImageWidth * 4,3),dtype=np.uint8)

    def connectImages(self):
        """Connects images previously set with method setImages"""
        widthOffset = self.singleImageWidth

        self.lastFrame[:,:widthOffset,:] = self.images["left"] if self.images["left"] is not None else 0
        self.lastFrame[:,widthOffset:widthOffset * 2,:] = self.images["front"] if self.images["front"] is not None else 0
        self.lastFrame[:,widthOffset*2:widthOffset*3,:] = self.images["right"] if self.images["right"] is not None else 0
        self.lastFrame[:,widthOffset*3:,:] = self.images["back"] if self.images["back"] is not None else 0
        return True


class ImageConnectorSquare(ImageConnectorBase):
    """Connector that connects images that on top are front and back, on bottom are left and right"""

    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)
    
    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight * 2,self.singleImageWidth * 2,3),dtype=np.uint8)

    def connectImages(self):
        """Connects images previously set with method setImages"""
        widthOffset = self.singleImageWidth
        heightOffset = self.singleImageHeight

        self.lastFrame[:heightOffset,:widthOffset,:] = self.images["front"] if self.images["front"] is not None else 0
        self.lastFrame[:heightOffset,widthOffset:,:] = self.images["back"] if self.images["back"] is not None else 0
        self.lastFrame[heightOffset:,:widthOffset,:] = self.images["left"] if self.images["left"] is not None else 0
        self.lastFrame[heightOffset:,widthOffset:,:] = self.images["right"] if self.images["right"] is not None else 0
        return True


class ImageConnectorVerticalSplit(ImageConnectorBase):
    """Connector that splits image in three columns"""

    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)

    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight * 2, self.singleImageWidth * 3, 3), dtype=np.uint8)

    def connectImages(self):
        """Connects images previously set with method setImages"""
        widthOffset = self.singleImageWidth
        heightOffset = self.singleImageHeight

        self.lastFrame[:heightOffset, widthOffset:widthOffset*2, :] = self.images["front"] if self.images["front"] is not None else 0
        self.lastFrame[heightOffset:, widthOffset:widthOffset*2, :] = self.images["back"] if self.images["back"] is not None else 0
        self.lastFrame[heightOffset//2:(heightOffset*3)//2, :widthOffset, :] = self.images["left"] if self.images["left"] is not None else 0
        self.lastFrame[heightOffset//2:(heightOffset*3)//2, widthOffset*2:, :] = self.images["right"] if self.images["right"] is not None else 0
        return True


class ImageConnectorHorizontalSplit(ImageConnectorBase):
    """Connector that splits image in three rows"""

    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)

    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight * 3, self.singleImageWidth * 2, 3), dtype=np.uint8)

    def connectImages(self):
        """Connects images previously set with method setImages"""
        widthOffset = self.singleImageWidth
        heightOffset = self.singleImageHeight

        self.lastFrame[:heightOffset, widthOffset//2:(widthOffset*3)//2, :] = self.images["front"] if self.images["front"] is not None else 0
        self.lastFrame[heightOffset*2:, widthOffset//2:(widthOffset*3)//2, :] = self.images["back"] if self.images["back"] is not None else 0
        self.lastFrame[heightOffset:heightOffset*2, :widthOffset, :] = self.images["left"] if self.images["left"] is not None else 0
        self.lastFrame[heightOffset:heightOffset*2, widthOffset:, :] = self.images["right"] if self.images["right"] is not None else 0
        return True
