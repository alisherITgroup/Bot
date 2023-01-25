BOT_NAME = "Puul_bot"
from db import DataBase
db = DataBase("db.sqlite3")
# channels
CHANNELS = []
channels = db.get_config()[2].split(",")
for channel in channels:
    CHANNELS.append(channel.strip())
BOT_TOKEN = db.get_config()[1] #"5545010658:AAFb9QkpsVVG87TKJRgYt9L0TLP6-lnEJM0"
links = db.get_config()[3].split(",")