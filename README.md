# LSB Steganography

This project implements Least Significant Bit (LSB) steganography, allowing users to hide secret messages within images and retrieve them later. The application is built using Streamlit and OpenCV, providing a user-friendly interface for encryption and decryption of messages.

## Live Demo

Try out the live demo: [LSB Steganography App](https://lsb-st3go.streamlit.app/)

## Features

- Encrypt a message by hiding it within an uploaded image
- Decrypt and retrieve hidden messages from encrypted images
- User-friendly web interface built with Streamlit
- Support for JPG and PNG image formats
- Download encrypted images for later use

## How It Works

LSB (Least Significant Bit) steganography works by replacing the least significant bit of each color channel in an image with bits from the secret message. This method allows for hiding information within an image with minimal visual change to the original image.

## Usage

1. **Encrypting a Message:**
   - Upload an image (JPG or PNG)
   - Enter the secret message
   - Click "Encrypt Message"
   - Download the encrypted image

2. **Decrypting a Message:**
   - Upload an encrypted image (PNG)
   - Click "Decrypt Message"
   - View the retrieved hidden message

## Installation

To run this project locally:

1. Clone the repository:
   ```
   git clone https://github.com/Techno-Furious/LSB-Steganography.git
   ```

2. Navigate to the project directory:
   ```
   cd LSB-Steganography
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```
   streamlit run streamapp.py
   ```

## Requirements

- Python 3.6+
- Streamlit
- OpenCV
- NumPy

