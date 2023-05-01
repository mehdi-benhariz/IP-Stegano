import cv2
import numpy as np


def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes):
        return ''.join([format(i, "08b") for i in data])
    elif isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")


def encode(image, secret_data, n_bits=2):
    # maximum bytes to encode
    n_bytes = image.shape[0] * image.shape[1] * 3 * n_bits // 8
    print("[*] Maximum bytes to encode:", n_bytes)
    print("[*] Data size:", len(secret_data))
    if len(secret_data) > n_bytes:
        raise ValueError(
            f"[!] Insufficient bytes ({len(secret_data)}), need bigger image or less data.")
    print("[*] Encoding data...")
    # add stopping criteria
    if isinstance(secret_data, str):
        secret_data += "====="
    elif isinstance(secret_data, bytes):
        secret_data += b"====="
    # convert data to binary
    binary_secret_data = to_bin(secret_data)
    # size of data to hide
    data_len = len(binary_secret_data)
    # use numpy functions for faster operations
    pixel_iter = np.nditer(image, flags=['multi_index'])
    for bit in range(n_bits):
        for pixel in pixel_iter:
            # modify the least significant bit only if there is still data to store
            if pixel_iter.multi_index[0] < data_len:
                pixel_bits = to_bin(pixel)
                # set the least significant bit of the pixel to the data bit
                pixel_bits[bit] = binary_secret_data[pixel_iter.multi_index[0]]
                # convert binary back to integer representation
                pixel_int = np.packbits(pixel_bits).astype(np.uint8)
                # update the pixel value in the image
                pixel[...] = pixel_int
            # if data is encoded, just break out of the loop
            if pixel_iter.multi_index[0] >= data_len:
                break
    return image


def decode(image_name, n_bits=1, in_bytes=False):
    print("[+] Decoding...")
    # read the image
    image = cv2.imread(image_name)
    binary_data = ""
    for bit in range(1, n_bits+1):
        for row in image:
            for pixel in row:
                r, g, b = to_bin(pixel)
                binary_data += r[-bit]
                binary_data += g[-bit]
                binary_data += b[-bit]
    # split by 8-bits
    all_bytes = [binary_data[i: i+8] for i in range(0, len(binary_data), 8)]
    # convert from bits to characters
    if in_bytes:
        # if the data we'll decode is binary data,
        # we initialize bytearray instead of string
        decoded_data = bytearray()
        for byte in all_bytes:
            # append the data after converting from binary
            decoded_data.append(int(byte, 2))
            if decoded_data[-5:] == b"=====":
                # exit out of the loop if we find the stopping criteria
                break
    else:
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "=====":
                break
    return decoded_data[:-5]


image = cv2.imread("peppers_color.tif")
secret_img = encode(image, "Hello Mehdi", n_bits=2)

cv2.imwrite("encoded.png", secret_img)

print(decode("encoded.png", n_bits=2))
