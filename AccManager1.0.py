# simple telegram bot for scanning qr and keeping stats
# need: pip install pyTelegramBotAPI pyzbar pillow opencv-python

import telebot
import pickle
import os
from pyzbar.pyzbar import decode
from PIL import Image
import cv2

TOKEN = 'YOUR_TOKEN_HERE'
bot = telebot.TeleBot(TOKEN)

if os.path.exists('stats.pkl'):
    stats = pickle.load(open('stats.pkl','rb'))
else:
    stats = {}

@bot.message_handler(commands=['start'])
def start(m):
    id = m.from_user.id
    if id not in stats:
        stats[id] = 0
        pickle.dump(stats, open('stats.pkl','wb'))
    bot.reply_to(m, "profile created, send me qr code photos")

@bot.message_handler(content_types=['photo'])
def photo(m):
    id = m.from_user.id
    file = bot.get_file(m.photo[-1].file_id)
    down = bot.download_file(file.file_path)
    with open('temp.jpg','wb') as f:
        f.write(down)
    img = cv2.imread('temp.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dec = decode(Image.fromarray(gray))
    os.remove('temp.jpg')
    if dec:
        num = dec[0].data.decode()
        stats[id] += 1
        pickle.dump(stats, open('stats.pkl','wb'))  # saving every time, not smart but works
        bot.reply_to(m, f"scanned {num}, total: {stats[id]}")
    else:
        bot.reply_to(m, "couldnt find qr code")

bot.polling()
