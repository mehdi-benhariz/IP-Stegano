import numpy as np
import random

# https://en.wikipedia.org/wiki/Visual_cryptography 

'''
This will split a grayscale image into multiple shares of noise that can be used together to return back
to a black and white version of the original image.

Parameters:
image: The image to split
shares: The number of shares of noisy images to create

Returns:
    1.) An array of the noisy shared images
    2.) The original image in black and white created from two randomly selected shares

Requirements/Assumptions: 
    1. The image must be grayscale
    2. The number of shares must be within [2,7]
'''
def SecretSharing(image, shares):

    # Retrieve the size of the image
    height, width = image.shape[:2]

    # Basic thresholding to force the image to be black and white
    image[image > 128] = 255
    image[image != 255] = 0

    # Initialize the shares images as arrays of zero
    shareImages = []
    for i in range(shares):
       shareImages.append(np.zeros((height, width), dtype=np.uint8))

    # Create the possible bit values
    bitValues = []
    for i in range(shares):
        bitValues.append(2**i)

    # For each pixel that is black, assign the shares with a corresponding bit
    # If the pixel is white, then assign the same bit for each share
    '''ex. If three shares...

        A black pixel corresponds to a matrix with all different bit values like the following:
    [[1, 0, 0], (share 1 = 4)
     [0, 1, 0], (share 2 = 2)
     [0, 0, 1], (share 3 = 1)
    ]
        A white pixel corresponds to a matrix with the same bit values like the following:
    [[1, 0, 0], (share 1 = 4)
     [1, 0, 0], (share 2 = 4)
     [1, 0, 0], (share 3 = 4)
    ]
    '''
    for i in range(height):
        for j in range(width):
            
            # Randomize the bits order for a black pixel
            random.shuffle(bitValues)

            for k in range(shares):
                # If pixel is black, assign it the random bit value
                if image[i, j] == 0:
                    shareImages[k][i, j] = bitValues[k]

                # If pixel is white, we use the same randomized bit value for each share's pixel
                else:
                    shareImages[k][i, j] = bitValues[0]

    # Multiply each pixel by a constant to add more contrast to pixels (with few shares, the image just appears black to the human eye)
    for i in range(shares):
       shareImages[i] = shareImages[i] * (256 // (2**shares))


    '''Returning to the original image by randomly selecting two of the shares'''
    restoredImage = np.zeros((height, width), dtype=np.uint8)

    # Just to prove that the original can be retrieved with any two of the shares, let's randomize which shares are compared
    randomShare1 = 0
    randomShare2 = 0
    while randomShare1 == randomShare2:
        randomShare1 = random.randint(0, shares - 1)
        randomShare2 = random.randint(0, shares - 1)

    # Any pixels that are equal should be white
    restoredImage[shareImages[randomShare1] == shareImages[randomShare2]] = 255

    return shareImages, restoredImage