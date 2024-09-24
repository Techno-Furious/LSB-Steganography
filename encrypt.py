import cv2
import numpy as np


def encrypt(img, message):
    binary_message = convert_message_to_binary(message)
    img, start_pos = write_decrypt_info(img, binary_message)
    img = write_message(img, binary_message, start_pos)
    return img


def convert_message_to_binary(message):
    return ''.join(format(ord(i), '08b') for i in message)


def write_decrypt_info(img, binary_message):
    length = len(binary_message)
    start_pos = 16  # Start position after the length information
    info = format(length, '016b')  # Convert length to 16-bit binary string

    for i in range(16):
        row = i // img.shape[1]
        col = i % img.shape[1]
        img[row, col, 0] = (img[row, col, 0] & 254) | int(info[i])

    return img, start_pos


def write_message(img, binary_message, start_pos):
    h, w = img.shape[:2]
    total_pixels = h * w

    if len(binary_message) > (total_pixels - start_pos) * 3:
        raise ValueError("Message is too long to be encoded in the image")

    index = 0
    for i in range(start_pos, total_pixels):
        row = i // w
        col = i % w
        for j in range(3):  # For each color channel
            if index < len(binary_message):
                img[row, col, j] = (img[row, col, j] & 254) | int(binary_message[index])
                index += 1
            else:
                return img
    return img


# Main execution
img_path = "test.jpg"
img = cv2.imread(img_path)

if img is None:
    print(f"Error: Could not read the image file at {'test.jpg'}")
else:
    h, w = img.shape[:2]
    print(f"The height is {h} and the width is {w}")

    message = input("Enter the message you want to hide: ")
    encrypted_img = encrypt(img, message)

    output_path = 'encrypted_image.png'
    cv2.imwrite(output_path, encrypted_img)
    print(f"The message has been encrypted and saved in {output_path}")