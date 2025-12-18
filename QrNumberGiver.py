# This script generates a random QR code with a unique number embedded in it.
# Then, it provides a way to scan that QR code from an image and extract the number.
# I spent a lot of time figuring out the libraries and handling the image processing.
# There might be some inefficiencies, but it works for my purposes.
# Dependencies: You need to install qrcode, Pillow, pyzbar, and opencv-python.
# Run 'pip install qrcode pillow pyzbar opencv-python' if not installed.

import qrcode
import random
from PIL import Image
from pyzbar.pyzbar import decode
import cv2  # Using OpenCV for some image preprocessing, though maybe not necessary.
import os

# Function to generate a random number and create a QR code from it.
def generate_random_qr(output_file='random_qr.png'):
    # Generate a random number between 100000 and 999999 for uniqueness.
    random_number = random.randint(100000, 999999)
    
    # Create QR code instance.
    qr = qrcode.QRCode(
        version=1,  # Keeping it simple with version 1.
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add the random number as data to the QR code.
    qr.add_data(str(random_number))  # Converting to string just in case.
    qr.make(fit=True)
    
    # Make the image.
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save the image to file.
    img.save(output_file)
    
    print(f"Generated QR code with number: {random_number} and saved to {output_file}")
    
    # Returning the number for verification, though in real use maybe not needed.
    return random_number

# Function to scan the QR code from an image and extract the assigned number.
def extract_number_from_qr(image_path):
    if not os.path.exists(image_path):
        print("Error: Image file not found!")  # Basic error check.
        return None
    
    # Load the image using OpenCV for preprocessing.
    img_cv = cv2.imread(image_path)
    
    # Convert to grayscale, which helps in decoding sometimes.
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    
    # Threshold the image to make it binary - this might not always be optimal.
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Now, convert back to PIL image for pyzbar, since it works better with PIL sometimes.
    img_pil = Image.fromarray(thresh)
    
    # Decode the QR code.
    decoded_objects = decode(img_pil)
    
    # Loop through decoded objects, though usually there's only one.
    for obj in decoded_objects:
        if obj.type == 'QRCODE':  # Check if it's a QR code.
            data = obj.data.decode('utf-8')
            try:
                assigned_number = int(data)  # Assuming it's a number.
                print(f"Extracted assigned number: {assigned_number}")
                return assigned_number
            except ValueError:
                print("Error: Data in QR is not a number!")
                return None
    
    # If no QR found, print a message.
    print("No QR code found in the image.")
    return None

# Main function to test the whole thing.
if __name__ == "__main__":
    # Generate the QR.
    qr_file = 'test_qr.png'
    original_number = generate_random_qr(qr_file)
    
    # Now extract it back.
    extracted = extract_number_from_qr(qr_file)
    
    # Check if they match, with a simple print.
    if extracted == original_number:
        print("Success: Numbers match!")
    else:
        print("Mismatch or error occurred.")
    
    # Clean up the file, but commented out for now.
    # os.remove(qr_file)