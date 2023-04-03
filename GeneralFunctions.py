import numpy as np

# This is for any general functions that could be applied across different steganography things

# Histogram equalization
def equalize_histogram(image):
    histogram = np.histogram(image, bins=np.arange(257), density=True)[0]
    cdf = np.cumsum(histogram)
    intensities = np.uint8(np.round(255. * cdf))
    return intensities[image]