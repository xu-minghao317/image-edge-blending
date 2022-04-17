import cv2 as cv
from CalculateDisplayImage import CalculateDisplayImage

CDI = CalculateDisplayImage()

##
# @brief
#
# This class displays blended images.


class MainDisplay(object):

    ##
    # @brief
    # Display the blended images.
    # @param img is the image blended with masks.
    def display(img):
        cv.imshow('img', img)
        cv.waitKey(0)
        cv.destroyAllWindows()

    # The constructor.
    def __init__(self):
        pass

    ## A class variable.
    # To store the blended images.
    res = CDI.getDisplayImage(CDI.calculate())

    display(res[0])
    # display(res[1])
