# CipherHide - Futuristic Steganography Tool

A modern, sleek steganography application built with PyQt5 that allows you to hide secret messages in various media types:

- Text encryption/decryption
- Image steganography
- Audio steganography
- Video steganography (demonstration)

## Features

- **Secure Encryption**: Uses Fernet symmetric encryption to protect your messages
- **Multiple Media Support**: Hide data in images, audio, and videos
- **Futuristic UI**: Clean, modern interface with a cyberpunk aesthetic
- **User-Friendly**: Simple workflow for all steganography operations

## Installation

1. Clone this repository:
```
git clone https://github.com/Naveenkumar-Dev-21/Cipher-Hide.git
cd Cipher-Hide
```

2. Create a virtual environment (recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

## Usage

Run the application:
```
python stego_pyqt.py
```

### Key Management
1. First, generate a new encryption key or select an existing one
2. The key is required for all encryption and decryption operations

### Text Encryption/Decryption
1. Enter text and select your key to encrypt
2. For decryption, paste encrypted text and select the same key

### Image Steganography
1. Select an image to use as the carrier
2. Enter your secret message
3. Select your encryption key
4. Hide the message in the image
5. To extract, select the image with hidden data and your key

### Audio Steganography
1. Select an audio file (WAV recommended for best results)
2. Enter your secret message
3. Select your encryption key
4. Hide the message in the audio
5. To extract, select the audio with hidden data and your key

### Video Steganography
Currently includes a demonstration of the concept.

## Requirements

- Python 3.6+
- PyQt5
- Other dependencies in requirements.txt
