import cv2
def retrieve_message_length(img):
    binary_length = ''
    h, w = img.shape[:2]

    for i in range(16):
        row = i // w
        col = i % w
        binary_length += str(img[row, col, 0] & 1)

    return int(binary_length, 2)


def retrieve_message(img):
    message_length = retrieve_message_length(img)
    print(f"Message length: {message_length} bits")

    binary_message = ''
    h, w = img.shape[:2]
    total_pixels = h * w

    index = 0
    for i in range(16, total_pixels):
        row = i // w
        col = i % w
        for j in range(3):  # For each color channel
            if index < message_length:
                binary_message += str(img[row, col, j] & 1)
                index += 1
            else:
                break
        if index >= message_length:
            break

    # Convert the binary message back to a string
    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        message += chr(int(byte, 2))

    return message


# Main execution
img_path = "encrypted_image.png"
img = cv2.imread(img_path)

if img is None:
    print(f"Error: Could not read the image file at {img_path}")
else:
    hidden_message = retrieve_message(img)
    print(f"Retrieved message: {hidden_message}")