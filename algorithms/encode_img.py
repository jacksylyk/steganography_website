import numpy as np
import pandas as pand
import os
import cv2
from matplotlib import pyplot as plt


def msgtobinary(msg):
    if type(msg) == str:
        result = ''.join([format(ord(i), "08b") for i in msg])

    elif type(msg) == bytes or type(msg) == np.ndarray:
        result = [format(i, "08b") for i in msg]

    elif type(msg) == int or type(msg) == np.uint8:
        result = format(msg, "08b")

    else:
        raise TypeError("Input type is not supported in this function")

    return result


# In[8]:


def encode_img_data(img):
    data = input("\nEnter the data to be Encoded in Image :")
    if (len(data) == 0):
        raise ValueError('Data entered to be encoded is empty')

    nameoffile = "img/encoded_image.jpg"

    no_of_bytes = (img.shape[0] * img.shape[1] * 3) // 8

    print("\t\nMaximum bytes to encode in Image :", no_of_bytes)

    if (len(data) > no_of_bytes):
        raise ValueError("Insufficient bytes Error, Need Bigger Image or give Less Data !!")

    data += '*^*^*'

    binary_data = msgtobinary(data)
    print("\n")
    print(binary_data)
    length_data = len(binary_data)

    print("\nThe Length of Binary data", length_data)

    index_data = 0

    for i in img:
        for pixel in i:
            r, g, b = msgtobinary(pixel)
            if index_data < length_data:
                pixel[0] = int(r[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[1] = int(g[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data < length_data:
                pixel[2] = int(b[:-1] + binary_data[index_data], 2)
                index_data += 1
            if index_data >= length_data:
                break
    cv2.imwrite(nameoffile, img)
    print("\nEncoded the data successfully in the Image and the image is successfully saved with name ", nameoffile)


# In[9]:


def decode_img_data(encoded_image_path):
    img = cv2.imread(encoded_image_path)
    if img is None:
        raise ValueError("Failed to load the encoded image.")

    data_binary = ""
    for i in img:
        for pixel in i:
            r, g, b = pixel[:3]  # Extract RGB values from the pixel
            r, g, b = msgtobinary(r), msgtobinary(g), msgtobinary(b)  # Convert each value to binary
            data_binary += r[-1]
            data_binary += g[-1]
            data_binary += b[-1]
            total_bytes = [data_binary[i: i + 8] for i in range(0, len(data_binary), 8)]
            decoded_data = ""
            for byte in total_bytes:
                decoded_data += chr(int(byte, 2))
                if decoded_data[-5:] == "*^*^*":
                    print(decoded_data)
                    print("\n\nThe Encoded data which was hidden in the Image was: ", decoded_data[:-5])
                    return


if __name__ == '__main__':
    image = cv2.imread("img/cover_image_small_40.jpg")
    encode_img_data(image)
    print(decode_img_data("img/encoded_image.jpg"))