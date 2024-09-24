import streamlit as st
import cv2
import numpy as np
import io


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

    message = ''
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        message += chr(int(byte, 2))

    return message

# Streamlit UI
st.title("LSB Steganography")
st.write("This is a simple implementation of Least Significant Bit (LSB) steganography.")

# Encrypt section
st.header("Encrypt a Message")
uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "png"])
if uploaded_image is not None:
    image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), cv2.IMREAD_COLOR)
    st.image(image, channels="BGR")

    message = st.text_area("Enter the message to hide:")
    if st.button("Encrypt Message"):
        try:
            encrypted_img = encrypt(image, message)
            st.markdown(f"**<span style='color:green;'>Message encrypted! Click the download button below to save the image in </span>** **<span style='color:red; font-size:20px;'><strong>PNG format</strong></span>** **<span style='color:green;'>to decrypt it later.</span>**", unsafe_allow_html=True)

            st.image(encrypted_img, channels="BGR", caption="Encrypted Image")

            # Convert the encrypted image to bytes
            is_success, buffer = cv2.imencode(".png", encrypted_img)
            io_buf = io.BytesIO(buffer)

            # Create a download button
            st.download_button(
                label="Download Encrypted Image",
                data=io_buf.getvalue(),
                file_name="encrypted_image.png",
                mime="image/png"
            )
        except Exception as e:
            st.error(f"Error: {str(e)}")


# Decrypt section
st.header("Decrypt a Message")
uploaded_encrypted_image = st.file_uploader("Upload an Encrypted Image", type=["png"])
if uploaded_encrypted_image is not None:
    encrypted_image = cv2.imdecode(np.fromstring(uploaded_encrypted_image.read(), np.uint8), cv2.IMREAD_COLOR)
    st.image(encrypted_image, channels="BGR")

    if st.button("Decrypt Message"):
        try:
            hidden_message = retrieve_message(encrypted_image)
            st.success(f"Retrieved message: {hidden_message}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

