import cv2
from cryptography.fernet import Fernet
import os
import base64


def encrypt_text(key, text):
    """
    Encrypt the given text using the given key.
    """
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()


def decrypt_text(key, text):
    """
    Decrypt the given text using the given key.
    """
    f = Fernet(key)
    return f.decrypt(text.encode()).decode()


def hide_text_in_image(image, text, key):
    """
    Hides the given text inside the given image using the LSB steganography technique.
    """
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    height, width = grayscale_image.shape[:2]

    text = encrypt_text(key, text)
    # Convert the text to binary
    binary_text = ''.join(format(ord(i), '08b') for i in text)

    # Check if the length of the binary text is greater than the number of pixels in the image
    if len(binary_text) > height * width:
        raise ValueError('Text is too long to be hidden inside the image')

    # Pad the binary text with zeros if necessary
    binary_text += '0' * ((height * width) - len(binary_text))

    # Convert the binary text to a list of integers
    binary_text = [int(binary_text[i:i+8], 2)
                   for i in range(0, len(binary_text), 8)]

    # Hide the binary text inside the image
    for i in range(height):
        for j in range(width):
            if len(binary_text) == 0:
                break
            pixel_value = grayscale_image[i, j]
            new_pixel_value = (pixel_value & ~1) | binary_text.pop(0)
            grayscale_image[i, j] = new_pixel_value

    # Return the steganographed image
    return grayscale_image


def retrieve_text_from_image(image, key):
    """
    Retrieve the text hidden inside the given image using the LSB steganography technique
    and decrypts it using the given key.
    """

    # grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscale_image = image

    height, width = grayscale_image.shape[:2]

    # Retrieve the binary text from the image
    binary_text = ''
    for i in range(height):
        for j in range(width):
            pixel_value = grayscale_image[i, j]
            binary_text += str(pixel_value & 1)

    # Convert the binary text to a string
    text = ''.join(chr(int(binary_text[i:i+8], 2))
                   for i in range(0, len(binary_text), 8))

    decrypted_text = decrypt_text(key, text)
    return decrypted_text


img = cv2.imread('peppers_color.tif')

key = base64.urlsafe_b64encode(os.urandom(32))

print(key)
# key = b"your 32-byte base64-encoded key here"
text = "Hello World"
steg_img = hide_text_in_image(img, text, key)
cv2.imwrite('steg_img.png', steg_img)

retrieved_text = retrieve_text_from_image(steg_img, key)
print(retrieved_text)
