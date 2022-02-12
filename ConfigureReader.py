from configparser import ConfigParser

##
# @brief
#
# This class reads initial values that will be needed to process the edge-blending.
# This class is made by Son and Minghao, Doxygened by Konatsu.
#


class ConfigureReader(object):

    # The constructor.
    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')

    ##
    # @brief
    # Get split image height.
    # @return image height in int.
    def getImageWidth(self):
        return int(self.config['DEFAULT']['ImageWidth'])

    ##
    # @brief
    # Get split image width.
    # @return image width in int.
    def getImageHeight(self):
        return int(self.config['DEFAULT']['ImageHeight'])

    ##
    # @brief
    # Get distance between two projectors.
    # @return projector distance in float.
    def getProjectorDistance(self):
        return float(self.config['DEFAULT']['projector_distance'])

    ##
    # @brief
    # Get projected image width.
    # @return image width in float.
    def getProjectorImageWidth(self):
        return float(self.config['DEFAULT']['projector_image_width'])

    ##
    # @brief
    # Get gamma value.
    # @return gamma value in float.
    def getGamma(self):
        return float(self.config['DEFAULT']['gamma'])

    ##
    # @brief
    # Get edge-blending method.
    # @return method in string.
    def getMethod(self):
        return str(self.config['DEFAULT']['method'])

    ##
    # @brief
    # Get image path (image should be put inside src).
    # @return image path in string.
    def getImagePath(self):
        return 'src/' + str(self.config['DEFAULT']['ImageNameLeft']), 'src/' + str(self.config['DEFAULT']['ImageNameRight'])

    # @var config
    # The configuration file.
