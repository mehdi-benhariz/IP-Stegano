import numpy as np

'''
This will "hide" a secondary black and white image in the first color image by replacing the least significant
bits in each color channel of the first image with corresponding bits in the black and white image.

Parameters:
image1- The color image
image2- The grayscale image
bits- How many bits to use when "hiding" the second image in the first

Returns:
An array with two elements:
    1. The first image that has the second image's information in its least significant bits
    2. The second image created only from the first image's least significant bits

Requirements/Assumptions: 
    1. The two images must be the same size. 
    2. The first image must have three channels and the second image must have one channel.
    3. bits must be either 1 or 2 (1 bit -> 8 intensities, 2 bit -> 64 intensities, 3 bit -> 512 intensities, which is too many!)
'''

def BitHidingGrayscale(image1, image2, bits):

    # Retrieve the size of the images
    height, width = image1.shape[:2]

    # Make a new zeros array that are the same size as the original images
    newImage1 = np.zeros((height, width, 3), dtype=np.uint8)
    newImage2 = np.zeros((height, width), dtype=np.uint8)

    # Examine each pixel
    for i in range(height):
        for j in range(width):
            # Convert the pixel in image2 to be a valid intensity level
            #   ex. if one bit is allowed, then there are only 8 valid intensity levels
            #   ex. if two bits are allowed, then there are 64 possible intensity levels
            pixelIntensity = format(int(image2[i, j] // (256 / (2**bits)**3)), '08b')
            
            # Take the least significant bits from image1 and store them in bin1
            bin1 = image1[i, j] % 2**bits
            
            # Take the corresponding binary bits for the given pixel intensity and splice it into thirds, placing that into bin2
            # ex. If using only 1 bit, then this splits 00000110 in binary into 1, 1, and 0   
            bin2 = [int(pixelIntensity[8 - 3 * bits:8 - 2 * bits]), int(pixelIntensity[8 - 2 * bits: 8 - bits]), 
                    int(pixelIntensity[8 - bits:])]

            # Assign the bits from image 2 into the least significant bits of image 1
            newImage1[i, j, 0] = image1[i, j, 0] - bin1[0] + bin2[0]
            newImage1[i, j, 1] = image1[i, j, 1] - bin1[1] + bin2[1]
            newImage1[i, j, 2] = image1[i, j, 2] - bin1[2] + bin2[2]

    '''Create the new second image'''
    # Notice how this image is created using solely from information contained in the first image
    for i in range(width):
        for j in range(height):
            # Retrieve the bits from the color channels
            bin3 = newImage1[i, j] % 2**bits    

            # Assign an intensity level using the retrieved bits      
            newImage2[i,j] = int((bin3[0] * 2**(bits * 2) + bin3[1] * 2**bits + bin3[2])) * (256 / (2**bits)**3)

    return [newImage1, newImage2]
