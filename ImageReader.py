import cv2 as cv
import numpy as np
from ConfigureReader import ConfigureReader

CR = ConfigureReader()

##
# @brief
#
# This class reads images and normalize them into numpy array tuple.
# This class is made by Shiva, Doxygened by Rikuto Momoi
#


class ImageReader(object):

    # The constructer
    def __init__(self):
        pass

    ##
    # @brief 
    # Get image in a normalized numpy array
    # @return normalized numpy array
    def getImage(self):
        return np.array(cv.imread(CR.getImagePath()[0]))/255, np.array(cv.imread(CR.getImagePath()[1]))/255
