import cv2
import numpy as np
import GeneralFunctions

'''
This will hide a print's information in a half tone version of the image.

Parameters:
serial: The printer's serial number to hide into the half tone result
image: The image to "print"
grayscale: Boolean that is true if the image is grayscale or false if colored

Returns:
    1.) A black image with the corresponding pixels containing the printer "code" on it
    2.) The first image converted to a half tone image that also has the printer information hidden in it
    3.) The information hidden in the printed image (date and time + serial number)

Requirements/Assumptions: 
    1. The serial number is 8 digits
    2. The image is at least 14 rows by 7 columns
'''

def PrinterHiding(serial, image, grayscale):

    # need 14 bits height for range 0-10000
    # need 7 colunns for dots (split serial # into two numbers)

    # Retrieve the size of the images
    height, width = image.shape[:2]

    # The dots will form a grid of 14 rows and 7 columns spread evenly
    rowsUsed = height // 27
    columnsUsed = width // 7

    # Retrieve date and time data
    data = GeneralFunctions.parseDateTime(27)

    # Append the serial code to the data
    data.append(format(int(serial), '27b').replace(' ', '0'))

    # Make a new zeros arrays that are the same size as the original image
    hiddenPrint = np.zeros((height, width), dtype=np.uint8)

    # Mark each pixel that needs to change to have the print "code"
    for i in range(7):
        for j in range(27):
                if data[i][j] == '1':
                    hiddenPrint[j * rowsUsed, i * columnsUsed] = 255

    finalPrint = image
    
    # Convert the grayscale image to bgr if the image is grayscale
    if grayscale:
        finalPrint = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    # Add the hidden print code to the image
    finalPrint[hiddenPrint == 255] = [14, 239, 233] # color yellow


    # Retrieve the hidden information from the finalPrint
    bits = np.zeros((7, 27), dtype=np.uint8)

    # Find each yellow pixel that corresponds to a bit in bits
    for i in range(7):
         for j in range(27):
              if finalPrint[j * rowsUsed, i * columnsUsed, 0] == 14 and finalPrint[j * rowsUsed, i * columnsUsed, 1] == 239 and finalPrint[j * rowsUsed, i * columnsUsed, 2] == 233:
                   bits[i][j] = '1'

    # Concatenate the bits together and convert to an int to get the day, month, year, hour, minute, second, and serial number
    day = int("".join([str(i) for i in bits[0]]).replace(' ', ''), 2)
    month = int("".join([str(i) for i in bits[1]]).replace(' ', ''), 2)
    year = int("".join([str(i) for i in bits[2]]).replace(' ', ''), 2)
    hour = int("".join([str(i) for i in bits[3]]).replace(' ', ''), 2)
    minute = int("".join([str(i) for i in bits[4]]).replace(' ', ''), 2)
    second = int("".join([str(i) for i in bits[5]]).replace(' ', ''), 2)
    serialNumber = int("".join([str(i) for i in bits[6]]).replace(' ', ''), 2)

    # Save the information in readable form
    hiddenInfo = str(day) + "/" + str(month) + "/" + str(year) + " " + str(hour) + ":" + str(minute) + ":" + str(second) + " #" + str(serialNumber)

    return [hiddenPrint, finalPrint, hiddenInfo]