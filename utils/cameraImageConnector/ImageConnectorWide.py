from ImageConnectorI import ImageConnectorBase
import numpy as np

class ImageConnector(ImageConnectorBase):
    
    def __init__(self, imageWidth, imageHeight):
        super().__init__(imageWidth, imageHeight)
    
    def _initFrame(self):
        self.lastFrame = np.zeros((self.singleImageHeight,self.singleImageWidth * self.cameraAmount,3),dtype=np.uint8)

    def connectImages(self):
        for i in range(len(self.images)):
            widthOffset = self.singleImageWidth * i
            self.lastFrame[:,widthOffset:self.singleImageWidth + widthOffset,:] = self.images[i]
        return True


        
    
