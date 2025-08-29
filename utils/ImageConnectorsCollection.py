import numpy as np
from typing import Optional
import cv2


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

    def setFpsInfo(self, camfps : dict, fps : int) -> None:
        """This method must be overridden with your image connection implementation"""
        pass
    

class ImageConnectorPanoramic(ImageConnectorBase):
    """Connector that connects images in a panoramic view"""

    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)
    
    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight + 50,self.singleImageWidth * 4,3),dtype=np.uint8)

    def connectImages(self):
        """Connects images previously set with method setImages"""
        widthOffset = self.singleImageWidth
        heightOffset = self.singleImageHeight

        self.lastFrame[:heightOffset,:widthOffset,:] = self.images["left"] if self.images["left"] is not None else 0
        self.lastFrame[:heightOffset,widthOffset:widthOffset * 2,:] = self.images["front"] if self.images["front"] is not None else 0
        self.lastFrame[:heightOffset,widthOffset*2:widthOffset*3,:] = self.images["right"] if self.images["right"] is not None else 0
        self.lastFrame[:heightOffset,widthOffset*3:,:] = self.images["back"] if self.images["back"] is not None else 0
        return True

    def setFpsInfo(self, camfps : dict, fps : int) -> None:
        """Pass the fps information and it will be displayed in frame"""
        self.lastFrame[self.singleImageHeight:, :] = 0
        textWithBorder(frame=self.lastFrame, text=f"        Camera front: {camfps['front']} fps          Camera back: "
                                                  f"{camfps['back']} fps          Camera left: {camfps['left']} fps    "
                                                  f"      Camera right: {camfps['right']} fps          Stream: {fps} fps",
                       pos=(0, self.singleImageHeight + 10), textColor=(255, 255, 255), borderColor=(200, 200, 200))


class ImageConnectorSquare(ImageConnectorBase):
    """Connector that connects images that on top are front and back, on bottom are left and right"""

    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)
    
    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight * 2 + 90,self.singleImageWidth * 2,3),dtype=np.uint8)

    def connectImages(self):
        """Connects images previously set with method setImages"""
        widthOffset = self.singleImageWidth
        heightOffset = self.singleImageHeight

        self.lastFrame[:heightOffset,:widthOffset,:] = self.images["front"] if self.images["front"] is not None else 0
        self.lastFrame[:heightOffset,widthOffset:,:] = self.images["back"] if self.images["back"] is not None else 0
        self.lastFrame[heightOffset:heightOffset*2,:widthOffset,:] = self.images["left"] if self.images["left"] is not None else 0
        self.lastFrame[heightOffset:heightOffset*2,widthOffset:,:] = self.images["right"] if self.images["right"] is not None else 0
        return True

    def setFpsInfo(self, camfps : dict, fps : int) -> None:
        """Pass the fps information and it will be displayed in frame"""
        self.lastFrame[self.singleImageHeight*2:, :] = 0
        textWithBorder(frame=self.lastFrame, text=f"    Camera front: {camfps['front']} fps    "
                                                  f"Camera back: {camfps['back']} fps      Stream: {fps} fps",
                       pos=(0, self.singleImageHeight * 2 + 10), textColor=(255, 255, 255), borderColor=(200, 200, 200))
        textWithBorder(frame=self.lastFrame, text=f"    Camera left: {camfps['left']} fps      "
                                                  f"Camera right: {camfps['right']} fps ",
                       pos=(0, self.singleImageHeight * 2 + 50), textColor=(255, 255, 255), borderColor=(200, 200, 200))


class ImageConnectorVerticalSplit(ImageConnectorBase):
    """Connector that splits image in three columns"""

    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)

    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight * 2 + 50, self.singleImageWidth * 3, 3), dtype=np.uint8)

    def connectImages(self):
        """Connects images previously set with method setImages"""
        widthOffset = self.singleImageWidth
        heightOffset = self.singleImageHeight

        self.lastFrame[:heightOffset, widthOffset:widthOffset*2, :] = self.images["front"] if self.images["front"] is not None else 0
        self.lastFrame[heightOffset:heightOffset*2, widthOffset:widthOffset*2, :] = self.images["back"] if self.images["back"] is not None else 0
        self.lastFrame[heightOffset//2:(heightOffset*3)//2, :widthOffset, :] = self.images["left"] if self.images["left"] is not None else 0
        self.lastFrame[heightOffset//2:(heightOffset*3)//2, widthOffset*2:, :] = self.images["right"] if self.images["right"] is not None else 0
        return True

    def setFpsInfo(self, camfps : dict, fps : int) -> None:
        """Pass the fps information and it will be displayed in frame"""
        self.lastFrame[self.singleImageHeight*2:, :] = 0
        textWithBorder(frame=self.lastFrame, text=f" Camera front: {camfps['front']} fps   Camera back: "
                                                  f"{camfps['back']} fps   Camera left: {camfps['left']} fps "
                                                  f"  Camera right: {camfps['right']} fps   Stream: {fps} fps",
                       pos=(0, self.singleImageHeight*2 + 10), textColor=(255, 255, 255), borderColor=(200, 200, 200))


class ImageConnectorHorizontalSplit(ImageConnectorBase):
    """Connector that splits image in three rows"""

    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)

    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight * 3 + 90, self.singleImageWidth * 2, 3), dtype=np.uint8)

    def connectImages(self):
        """Connects images previously set with method setImages"""
        widthOffset = self.singleImageWidth
        heightOffset = self.singleImageHeight

        self.lastFrame[:heightOffset, widthOffset//2:(widthOffset*3)//2, :] = self.images["front"] if self.images["front"] is not None else 0
        self.lastFrame[heightOffset*2:heightOffset*3, widthOffset//2:(widthOffset*3)//2, :] = self.images["back"] if self.images["back"] is not None else 0
        self.lastFrame[heightOffset:heightOffset*2, :widthOffset, :] = self.images["left"] if self.images["left"] is not None else 0
        self.lastFrame[heightOffset:heightOffset*2, widthOffset:, :] = self.images["right"] if self.images["right"] is not None else 0
        return True

    def setFpsInfo(self, camfps : dict, fps : int) -> None:
        """Pass the fps information and it will be displayed in frame"""
        self.lastFrame[self.singleImageHeight*3:, :] = 0
        textWithBorder(frame=self.lastFrame, text=f"    Camera front: {camfps['front']} fps    "
                                                  f"Camera back: {camfps['back']} fps      Stream: {fps} fps",
                       pos=(0, self.singleImageHeight * 3 + 10), textColor=(255, 255, 255), borderColor=(200, 200, 200))
        textWithBorder(frame=self.lastFrame, text=f"    Camera left: {camfps['left']} fps      "
                                                  f"Camera right: {camfps['right']} fps ",
                       pos=(0, self.singleImageHeight * 3 + 50), textColor=(255, 255, 255), borderColor=(200, 200, 200))
        

class ImageConnectorOneImage(ImageConnectorBase):
    """Only one image"""

    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)

    def _initFrame(self):
        print(f"Width:{self.singleImageWidth} Height:{self.singleImageHeight}")
        self.lastFrame = np.zeros((self.singleImageHeight , self.singleImageWidth , 3), dtype=np.uint8)

    def connectImages(self):
        """Connects images previously set with method setImages"""
        self.lastFrame = self.images["right"] if self.images["right"] is not None else 0
        return True

    def setFpsInfo(self, camfps : dict, fps : int) -> None:
        """Pass the fps information and it will be displayed in frame"""
        return None


def textWithBorder(frame, text = "", pos = (0,0), textColor = (0,0,0), borderColor = (128,128,128), fontSize = 1):
#   _, h = cv2.getTextSize(text,cv2.FONT_HERSHEY_COMPLEX,fontSize,6)[0]
#   cv2.putText(frame,text,(pos[0],pos[1]+h),cv2.FONT_HERSHEY_COMPLEX,fontSize,borderColor,3)
#   cv2.putText(frame,text,(pos[0],pos[1]+h),cv2.FONT_HERSHEY_COMPLEX,fontSize,textColor,1)
    return None
