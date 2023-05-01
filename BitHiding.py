import numpy as np
import GeneralFunctions

'''
This will "hide" a secondary image in the first image by replacing the least significant
bits in the first image with the most significant bits in the second image for each
channel.

Parameters:
image1- The first image
image2- The second image
bits- How many bits to use when "hiding" the second image in the first

Returns:
An array with three elements:
    1. The first image that has the second image's information in its least significant bits
    2. The second image created only from the first image's least significant bits
    3. A weighted average of the second image to attempt to closer match the original image2

Requirements/Assumptions: 
    1. The two images must be the same size. 
    2. The images must have three channels. 
    3. bits must be between 1 and 8
'''


def BitHiding(image1, image2, bits):

    # Retrieve the size of the images
    height, width = image1.shape[:2]

    # Make a new zeros array that are the same size as the original images
    newImage1 = np.zeros((height, width, 3), dtype=np.uint8)

    # Examine each pixel
    for i in range(height):
        for j in range(width):
            # Take the least significant bits from image1
            bin1 = image1[i, j] % 2**bits

            # Take the most significant bits from image2
            bin2 = [int(image2[i, j, 0] * 2**bits / 256), int(image2[i, j, 1] * 2**bits / 256), int(image2[i, j, 2] * 2**bits / 256)]

            # Assign the most significant bits from image 2 into the least significant bits of image 1
            newImage1[i, j, 0] = image1[i, j, 0] - bin1[0] + bin2[0]
            newImage1[i, j, 1] = image1[i, j, 1] - bin1[1] + bin2[1]
            newImage1[i, j, 2] = image1[i, j, 2] - bin1[2] + bin2[2]

    '''Create the new second image'''
    # Notice how this image is created using solely from information contained in the first image
    newImage2 = np.array(newImage1 % 2**bits * 256 / 2**bits, dtype=np.uint8)

    # Take a weighted average of the newImage2 and the histogram equalized newImage2
    modifiedImage2 = GeneralFunctions.equalize_histogram(newImage2) // 3 + newImage2 // 2

    return [newImage1, newImage2, modifiedImage2]
