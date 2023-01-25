from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from configfile import CHANNELS, links
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, input_field_placeholder="")
shareMenu = ReplyKeyboardMarkup(resize_keyboard=True)
btnShare = KeyboardButton("🔗Do'stlarga ulashish")
btnProfile = KeyboardButton("👤Profil")
rtProfile = KeyboardButton("📈Reyting")
stProfile = KeyboardButton("📊Statistika")
admin = KeyboardButton("📝Adminga yozish")
share = KeyboardButton("📞Raqamni ulashish")
share_keyboard = KeyboardButton(text="Share", request_contact=True)
mainMenu.add(btnShare, btnProfile)
mainMenu.add(rtProfile, stProfile)
mainMenu.add(admin, share)
shareMenu.add(share_keyboard)
check = InlineKeyboardButton(
    text="Tekshirish",
    callback_data="subdone"
)
btn_group = InlineKeyboardMarkup(row_width=1)
for link in links:
    if links.index(link) == 0:
        urlLink = InlineKeyboardButton(
        text="Instagram",
        url=link.strip()
        )
    elif links.index(link) == 1:
        urlLink = InlineKeyboardButton(
            text="YouTube",
            url=link.strip()
        )
    else:
        urlLink = InlineKeyboardButton(
            text="O'yin",
            url=link.strip()
        )
    btn_group.insert(urlLink)
for channel in CHANNELS:
    urlChannelBtn = InlineKeyboardButton(
    text=f"{channel[1::]}",
    url=f"https://t.me/{channel[1::]}"
)
    btn_group.insert(urlChannelBtn)

btn_group.insert(check)