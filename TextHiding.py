import cv2
import numpy as np


def hide_text_in_image(image, secret_text):
    # Convert secret text to binary string
    secret_bin = ''.join(format(ord(c), '08b')
                         for c in secret_text) + '11111111'

    # Modify least significant bit of each pixel in image to embed secret message
    flat_image = image.ravel()
    for i, bit in enumerate(secret_bin):
        if i >= len(flat_image) * 0.75:
            break
        flat_image[i] = (flat_image[i] & 254) | int(bit)

    # Reshape modified image back to original dimensions
    return flat_image.reshape(image.shape)


def extract_text_from_image(image):
    # Extract least significant bit of each pixel in image
    flat_image = image.ravel()
    secret_bin = ''
    for pixel in flat_image:
        secret_bin += str(pixel & 1)

    # Convert binary string to text
    secret_text = ''
    for i in range(0, len(secret_bin), 8):
        byte = secret_bin[i:i+8]
        if byte == '11111111':
            break
        secret_text += chr(int(byte, 2))

    return secret_text


# * hide the text in the image
# img = cv2.imread('peppers_color.tif')
# secret_text = "This is a secret message!"
# steg_img = hide_text_in_image(img, secret_text)
# cv2.imwrite('steg_peppers.png', steg_img)
# cv2.imshow('steg_peppers.png', steg_img)
# * extract the text from the image
hidden_img = cv2.imread('steg_peppers.png')
hidden_text = extract_text_from_image(hidden_img)
print(hidden_text)
