# This is a simple Telegram bot in Python that allows users to create profiles and track how many QR codes they've scanned.
# I used telebot library for the bot, and pyzbar for decoding QR from images.
# Also, using pickle to save the user data to a file, not the best but works for small scale.
# Spent time figuring out how to handle images and decode them properly.
# There are some parts that could be optimized, like error handling, but it runs okay.
# Dependencies: pip install pyTelegramBotAPI pyzbar pillow
# You need to replace 'YOUR_BOT_TOKEN' with your actual token from BotFather.

import telebot
import pickle
from pyzbar.pyzbar import decode
from PIL import Image
import os
import cv2  # Added OpenCV for preprocessing, similar to previous script.

# Bot token - replace with yours.
BOT_TOKEN = 'YOUR_BOT_TOKEN'

# File to store user data.
DATA_FILE = 'user_stats.pkl'

# Global dictionary for user stats: user_id -> {'profile_created': True, 'qr_scanned': count}
user_stats = {}

# Load data from file if exists.
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'rb') as f:
        user_stats = pickle.load(f)  # No error handling here, assuming file is good.

# Initialize the bot.
bot = telebot.TeleBot(BOT_TOKEN)

# Handler for /start command to create profile.
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in user_stats:
        user_stats[user_id] = {'profile_created': True, 'qr_scanned': 0}
        save_data()  # Save after creating.
        bot.reply_to(message, "Profile created! You can now send me QR code images to scan.")
    else:
        bot.reply_to(message, "You already have a profile. Send QR images to scan.")

# Handler for /stats command to show statistics.
@bot.message_handler(commands=['stats'])
def stats(message):
    user_id = message.from_user.id
    if user_id in user_stats:
        count = user_stats[user_id]['qr_scanned']
        bot.reply_to(message, f"You have scanned {count} QR codes so far.")
    else:
        bot.reply_to(message, "No profile found. Use /start to create one.")

# Handler for photo messages - assuming the photo contains a QR code.
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    if user_id not in user_stats:
        bot.reply_to(message, "Please create a profile first with /start.")
        return
    
    # Get the photo file_id.
    file_info = bot.get_file(message.photo[-1].file_id)  # Taking the largest photo.
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Save temporarily to decode.
    temp_file = 'temp_qr.jpg'
    with open(temp_file, 'wb') as f:
        f.write(downloaded_file)
    
    # Now decode the QR.
    extracted = extract_number_from_qr(temp_file)
    
    # Clean up the temp file.
    os.remove(temp_file)
    
    if extracted is not None:
        user_stats[user_id]['qr_scanned'] += 1
        save_data()  # Save after each scan, not efficient but simple.
        bot.reply_to(message, f"QR scanned successfully! Extracted number: {extracted}. Total scanned: {user_stats[user_id]['qr_scanned']}")
    else:
        bot.reply_to(message, "Couldn't find a valid QR code in the image.")

# Function to extract number from QR, copied from previous script with minor tweaks.
def extract_number_from_qr(image_path):
    if not os.path.exists(image_path):
        print("Error: Image file not found!")  # Print to console, not to user.
        return None
    
    # Load with CV2.
    img_cv = cv2.imread(image_path)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # To PIL.
    img_pil = Image.fromarray(thresh)
    
    # Decode.
    decoded_objects = decode(img_pil)
    
    for obj in decoded_objects:  # Loop even if one.
        if obj.type == 'QRCODE':
            data = obj.data.decode('utf-8')
            try:
                assigned_number = int(data)
                return assigned_number
            except ValueError:
                return None
    
    return None

# Function to save data to file.
def save_data():
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(user_stats, f)  # Dumping the whole dict each time, not optimized for large data.

# Start polling.
if __name__ == "__main__":
    print("Bot is running...")  # Console message.
    bot.polling(none_stop=True)  # Polling with none_stop, typo in param but it works as non_stop.