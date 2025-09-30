import qrcode
from PIL import Image
import string
import random
import os

def generate_random_string(length=10):
    """Generate a random string of specified length."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_random_color():
    """Generate a random RGB color."""
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generate_qr_code(data=None, filename="qrcode.png", random_data=False, random_length=10, random_style=True):
    """
    Generate a QR code with the specified or random data, with optional randomized visual style.
    
    Args:
        data (str): The data to encode in the QR code (e.g., URL, text). If None and random_data=True, a random string is generated.
        filename (str): The output filename for the QR code image (default: 'qrcode.png').
        random_data (bool): If True, generates random data for the QR code (default: False).
        random_length (int): Length of the random string if random_data is True (default: 10).
        random_style (bool): If True, randomizes mask pattern and colors for visual variety (default: True).
    
    Returns:
        bool: True if QR code is generated successfully, False otherwise.
    """
    try:
        # Generate random data if specified or if data is None
        if random_data or data is None:
            data = generate_random_string(random_length)
            print(f"Generated random data: {data}")
        
        # Validate input data
        if not isinstance(data, str) or not data.strip():
            raise ValueError("Data must be a non-empty string.")
        
        # Validate filename
        if not filename.endswith(('.png', '.jpg', '.jpeg')):
            filename = filename + '.png'
        
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            mask_pattern=random.randint(0, 7) if random_style else None  # Random mask pattern (0-7)
        )
        
        # Add data to QR code
        qr.add_data(data)
        qr.make(fit=True)
        
        # Set colors (random if random_style is True, otherwise default)
        fill_color = get_random_color() if random_style else "black"
        back_color = get_random_color() if random_style else "white"
        
        # Ensure fill and background colors are different for readability
        while random_style and fill_color == back_color:
            back_color = get_random_color()
        
        # Create image from QR code
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        
        # Save the QR code image
        img.save(filename)
        print(f"QR code saved as {filename} with data: {data}")
        return True
    
    except Exception as e:
        print(f"Error generating QR code: {str(e)}")
        return False

# Example usage
if __name__ == "__main__":
    # Example 1: Generate QR code with random data and random style
    #generate_qr_code(random_data=True, filename="random_qr.png", random_length=12, random_style=True)
    
    # Example 2: Generate QR code with specific data and random style
    generate_qr_code(
        data="https://example.com",
        filename="example_qr.png",
        random_style=True
    )