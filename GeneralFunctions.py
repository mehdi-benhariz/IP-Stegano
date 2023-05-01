import numpy as np
from datetime import datetime

# This is for any general functions that could be applied across different steganography methods

# Histogram equalization
def equalize_histogram(image):
    histogram = np.histogram(image, bins=np.arange(257), density=True)[0]
    cdf = np.cumsum(histogram)
    intensities = np.uint8(np.round(255. * cdf))
    return intensities[image]

# Get the day, month, year, hour, minute, and second with the option to format the data in binary form
def parseDateTime(binaryDigits = 0):

    dateTime = []

    # Set up binary digits
    binaryFormat = ""
    if binaryDigits > 9:
        binaryFormat = str(binaryDigits) + 'b'
    else:
        binaryFormat = '0' + str(binaryDigits) + 'b'

    dateTime.append(int(datetime.now().strftime("%d"))) # day
    dateTime.append(int(datetime.now().strftime("%m"))) # month
    dateTime.append(int(datetime.now().strftime("%Y"))) # year
    dateTime.append(int(datetime.now().strftime("%H"))) # hour
    dateTime.append(int(datetime.now().strftime("%M"))) # minute
    dateTime.append(int(datetime.now().strftime("%S"))) # second

    # Do binary conversion if necessary
    if binaryDigits > 0:
        for i in range(6):
            dateTime[i] = format(dateTime[i], binaryFormat).replace(' ', '0')
    
    return dateTime
