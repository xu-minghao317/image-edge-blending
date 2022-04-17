import cv2 as cv
import numpy as np
from ConfigureReader import ConfigureReader
from ImageReader import ImageReader

CR = ConfigureReader()
IR = ImageReader()

##
# @brief
#
# This class calculates blended image.


class CalculateDisplayImage(object):

    # The constructor
    def __init__(self):
        projector_image_width = CR.getProjectorImageWidth()
        projector_distance = CR.getProjectorDistance()
        self.image_width = CR.getImageWidth()
        self.image_height = CR.getImageHeight()
        self.gamma = CR.getGamma()
        self.method = CR.getMethod()
        self.np_left = IR.getImage()[0]
        self.np_right = IR.getImage()[1]
        self.overlap_pixels = round(
            self.image_width*(projector_image_width - projector_distance)/projector_image_width)

    ##
    # @brief
    # Get the blended image.
    # @param corrected_tuple contains the gamma corrected image left and right.
    # @return RGB formatted blended images.
    def getDisplayImage(self, corrected_tuple):
        corrected_left, corrected_right = corrected_tuple
        # to RGB
        blended_left = np.rint(corrected_left*255).astype(np.uint8)
        blended_right = np.rint(corrected_right*255).astype(np.uint8)
        # save images
        cv.imwrite('src/blended_left.jpg', blended_left)
        cv.imwrite('src/blended_right.jpg', blended_right)
        return blended_left, blended_right

    ##
    # @brief
    # Control the texture of the mask.
    # @param distance is the distance from the start point of the target overlap region.
    # @param monotonicity is the monotonicity of the intensity function.
    # @return Intensity control value.
    def intensityController(self, distance, monotonicity):

        if monotonicity == 'linearly_increase':
            return -distance/self.overlap_pixels + 1
        elif monotonicity == 'linearly_decrease':
            return distance/self.overlap_pixels
        elif monotonicity == 'nonlinearly_increase':
            return -np.power(distance/self.overlap_pixels, 2) + 1
        elif monotonicity == 'nonlinearly_decrease':
            return np.power(distance/self.overlap_pixels, 2)

    ##
    # @brief
    # Generates masks.
    # @param direction is the direction of the mask.
    # @return Gradient masks (in linear case).
    def maskGenerator(self, direction):
        
        # assume images have the same size
        mask = np.ones(self.np_left.shape)
        for columns in range(self.image_width-self.overlap_pixels-1, self.image_width):
            mask[0, columns, :] *= self.intensityController(
                columns-(self.image_width-self.overlap_pixels-1), monotonicity=self.method+'ly_increase')
        # replacement is more efficient than multiplication
        for rows in range(1, self.image_height):
            mask[rows, :, :] = mask[0, :, :]

        if direction == 'left':
            return mask
        elif direction == 'right':
            # flip direction of mask to right
            return np.flip(mask, axis=1)

    ##
    # @brief
    # Get gamma corrected image.
    # @param img is the image blended with masks.
    # @param direction is the direction of the image.
    # @param gamma is the gamma value.
    # @return Gamma corrected numpy array.
    def gammaCorrection(self, img, direction, gamma):

        if direction == 'left':
            for rows in range(self.image_height):
                for columns in range(self.image_width-self.overlap_pixels-1, self.image_width):
                    img[rows][columns][:] *= np.power(self.intensityController(
                        columns-(self.image_width-self.overlap_pixels-1), monotonicity=self.method + 'ly_increase'), gamma)
            return img

        elif direction == 'right':
            for rows in range(self.image_height):
                for columns in range(self.overlap_pixels-1):
                    img[rows][columns][:] *= np.power(
                        self.intensityController(columns, monotonicity=self.method + 'ly_decrease'), gamma)
            return img

    ##
    # @brief
    # Calculate the image to display.
    # @return final blended image left and right.
    def calculate(self):
        # generate masks
        mask_left = self.maskGenerator(
            direction='left')
        mask_right = self.maskGenerator(
            direction='right')
        # blend images with masks
        with_mask_left = np.multiply(self.np_left, mask_left)
        with_mask_right = np.multiply(self.np_right, mask_right)
        # apply gamma correction
        corrected_left = self.gammaCorrection(
            with_mask_left, direction='left', gamma=self.gamma)
        corrected_right = self.gammaCorrection(
            with_mask_right, direction='right', gamma=self.gamma)
        return corrected_left, corrected_right

    ## @var gamma
    # Gamma value.
    ## @var method
    # Method of intensity control.
    ## @var np_left
    # Normalized Numpy array of left image.
    ## @var np_right
    # Normalized Numpy array of right image.
    ## @var overlap_pixels
    # Overlap region width.
    ## @var image_height
    # Image height.
    ## @var image_width
    # Image width.
