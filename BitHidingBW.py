import numpy as np

'''
This will "hide" a secondary black and white image in the first color image by replacing the least significant
bits in each color channel of the first image with corresponding bits in the black and white image.

Parameters:
image1- The color image
image2- The black and white image
bits- How many bits to use when "hiding" the second image in the first

Returns:
An array with two elements:
    1. The first image that has the second image's information in its least significant bits
    2. The second image created only from the first image's least significant bits

Requirements/Assumptions: 
    1. The two images must be the same size. 
    2. The first image must have three channels and the second image must have one channel.
    3. bits must be between 1 and 3 (1 bit -> 8 intensities, 2 bit -> 64 intensities, 3 bit -> 512 intensities)
        Note: if three bits are selected, then the red channel will only use 2 bits
'''

def BitHidingBW(image1, image2, bits):

    # Retrieve the size of the images
    height, width = image1.shape[:2]

    # Make a new zeros array that are the same size as the original images
    newImage1 = np.zeros((height, width, 3), dtype=np.uint8)
    newImage2 = np.zeros((height, width), dtype=np.uint8)

    # Examine each pixel
    for i in range(height):
        for j in range(width):
            # Take the least significant bits from image1
            bin1 = [int(image1[i, j, 0] % 2**bits), int(image1[i, j, 1] %
                                                        2**bits), int(image1[i, j, 2] % 2**bits)]

            # Take the binary adjusted value at the pixel in image 2
            # ex. if one bit allocated, pixel intensity needs to be divided by 32 and converted to binary
            #       (32 is (2^1)^3), where 2 is one binary bit, 1 is how many bits, and 3 is the three channels
            pixelIntensity = format(int(image2[i, j] // (256 / (2**bits)**3)), '08b')
            
            # Take the corresponding binary bits for the given pixel intensity
            # ex. if one bit is allocated
             # TODO FIX THIS FOR 3 BITS!!!
            bin2 = [int(pixelIntensity[8 - 3 * bits:8 - 2 * bits]), int(pixelIntensity[8 - 2 * bits: 8 - bits]), 
                    int(pixelIntensity[8 - bits:])]

            # Assign the most significant bits from image 2 into the least significant bits of image 1
            newImage1[i, j, 0] = image1[i, j, 0] - bin1[0] + bin2[0]
            newImage1[i, j, 1] = image1[i, j, 1] - bin1[1] + bin2[1]
            newImage1[i, j, 2] = image1[i, j, 2] - bin1[2] + bin2[2]

    # Create the new second image
    # Notice how this image is created using solely from information contained in the first image
    for i in range(width):
        for j in range(height):

            bin3 = [int(newImage1[i, j, 0] % 2**bits), int(newImage1[i, j, 1] % 2**bits), int(newImage1[i, j, 2] % 2**bits)]          
            newImage2[i,j] = int((bin3[0] * 2**(bits * 2) + bin3[1] * 2**bits + bin3[2])) * (256 / (2**bits)**3)

    return [newImage1, newImage2]
