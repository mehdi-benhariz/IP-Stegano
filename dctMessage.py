import numpy as np
import cv2
import random
import re
from scipy.fft import dctn, idctn

'''
This will hide a message in the discrete cosine transformation of the image, then perform the inverse dct.

Parameters:
image: The image to hide the message in
message: The message to hide

Returns:
    1.) The image with the altered dct that hides a message
    2.) The message retrived from the image

Requirements/Assumptions: 
    1. The image must be grayscale
    2. The message must use only [a-zA-Z]
'''

def dctMessage(image, message_):

    # Get the height and width of the image
    height, width = image.shape[:2]

    # Get a random position in an 8x8 grid to hide bits (will be used later)
    bitHidingLocation = random.randint(0, 63)

    # Randomly get the first 8x8 position in the image to begin hiding the message in
    firstPosition = random.randint(0, int(height * width / 64) - 1)

    # 15 most frequently used letters in the English language
    replacementLetters = ['a', 'c', 'd', 'e', 'f', 'h', 'i', 'l', 'm', 'n', 'o', 'r', 's', 't', 'u']
    replacementLettersIndex = [0, 2, 1, 2, 3, 4, 10, 5, 6, 6, 1, 7, 8, 9, 10, 10, 10, 11, 12, 13, 14, 14, 14, 12, 12, 12]

    # Remove spaces and replace uppercase with lowercase
    message = list(re.sub("\s", "", message_.lower()))

    # Convert the message into a reduced alphabet and convert to binary
    for i in range(len(message)):
        message[i] = format(replacementLettersIndex[ord(message[i]) - 97], '04b')

    # Create the dct of the image
    dctImage = dctn(image)

    for i in range(len(message)):
        for j in range(2):

            # Get the selected 8x8 block, originally starting at the randomized firstPosition
            selection = dctImage[(firstPosition // 8 + i * 8) % height:(firstPosition // 8 + i * 8) % height + 8, (firstPosition % 8 + j * 8) % width:(firstPosition % 8 + j * 8) % width + 8]
            
            # Retrieve the specific value at the randomized BitHidingLocation
            value = selection[bitHidingLocation // 8, bitHidingLocation % 8]

            # Assigning the first or last two bits to the 5th place after decimal (fifth place is arbitrary)
            if value > 0:
                if j == 0:
                    value = value - float('0.0000' + str(value).split('.')[1][4]) + int(message[i][0:2], 2) * 10**-5
                else:
                    value = value - float('0.0000' + str(value).split('.')[1][4]) + int(message[i][2:], 2) * 10**-5
            else:
                if j == 0:
                    value = value - float('-0.0000' + str(value).split('.')[1][4]) - int(message[i][0:2], 2) * 10**-5
                else:
                    value = value - float('-0.0000' + str(value).split('.')[1][4]) - int(message[i][2:], 2) * 10**-5

            # Assign the modified value back into the dct
            dctImage[(firstPosition // 8 + i * 8) % height + bitHidingLocation // 8, (firstPosition % 8 + j * 8) % width + bitHidingLocation % 8] = value

    # Get the image back after inverse dct and some thresholding
    hiddenMsgImage = idctn(dctImage)
    hiddenMsgImage[hiddenMsgImage > 255.] = 255.
    hiddenMsgImage[hiddenMsgImage < 0.] = 0.


    '''Retrieving the secret message'''

    # Convert the image back to the dct
    dctImage = dctn(hiddenMsgImage)

    retrievedMessage = ""

    # Retrieve the message
    for i in range(len(message)):

        # Temporary string to hold the binary values of the 
        tempStr = ""
        for j in range(2):

            # Get the number at the fifth digit past the decimal based on the randomized starting position
            tempStr = tempStr + format(int(str(dctImage[(firstPosition // 8 + i * 8) % height + bitHidingLocation // 8, (firstPosition % 8 + j * 8) % width + bitHidingLocation % 8]).split('.')[1][4]), '02b')

        # Convert the binary digit to an int and retrieve the corresponding letter
        retrievedMessage = retrievedMessage + replacementLetters[int(tempStr, 2)]


    return hiddenMsgImage, retrievedMessage


