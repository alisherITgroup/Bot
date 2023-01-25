from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, executor, types
from configfile import BOT_TOKEN, BOT_NAME,CHANNELS
from aiogram.dispatcher import FSMContext
from markups import mainMenu, btn_group, shareMenu
from db import DataBase
import logging
import re

class PhoneNumber(StatesGroup):
    number = State()

def is_uzb(text):
    pettern = r"(?:\+[9]{2}[8][0-9]{2}[0-9]{3}[0-9]{2}[0-9]{2})"
    isUzb = re.match(pettern, text)
    if isUzb:
        return True
    return False

def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    return False
logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = DataBase("db.sqlite3")

async def check_sub_channels(channels: list, user_id:int) -> bool:
    status = False
    for channel in channels:
        data = dict(await bot.get_chat_member(channel, user_id))
        if data["status"] != "left":
            status = True
            continue
        else:
            status = False
            break
    return status
@dp.message_handler(commands='start')
async def handler(message: types.Message):
    if message.chat.type == "private":
        if not db.user_exists(message.from_user.username):
            start_command = message.text
            referred_id = str(start_command[7:])
            if str(referred_id) != "":
                if str(referred_id) != str(message.from_user.id):
                    db.add_user(username=message.from_user.username, user_id=message.from_user.id, referrer_id=referred_id)
                    try:
                        await bot.send_message(referred_id, "Tabriklaymiz, taklif qilgan do'stlaringiz soni yan bittaga oshdi.")
                    except:
                        ...
                else:
                    await bot.send_message(message.from_user.id, "Referrall")
            else:
                    db.add_user(username=message.from_user.username, user_id=message.from_user.id, referrer_id="1")
        if await check_sub_channels(CHANNELS, message.from_user.id):
            await bot.send_message(message.from_user.id, "Assalomu alaykum! Puul botga xush kelibsiz. Bizning botimizga o'z do'stlaringizni taklif qiling va qimmatbaho yutuqlarga ega bo'ling.", reply_markup=mainMenu)
            print(db.user_exists(message.from_user.username))
            if not db.user_exists(message.from_user.username):
                start_command = message.text
                referred_id = str(start_command[7:])
                print(start_command)
                print(referred_id)
                if str(referred_id) != "":
                    if str(referred_id) != str(message.from_user.id):
                        db.add_user(username=message.from_user.username, user_id=message.from_user.id, referrer_id=referred_id)
                        try:
                            await bot.send_message(referred_id, "Tabriklaymiz, taklif qilgan do'stlaringiz soni yan bittaga oshdi.")
                        except:
                            ...
                    else:
                        await bot.send_message(message.from_user.id, "Referrall")
                else:
                    db.add_user(username=message.from_user.username, user_id=message.from_user.id, referrer_id="1")
        else:
            await bot.send_message(message.from_user.id, "Kechirasiz! Bot to'liq foydalanish uchun kanallarimizga obuna bo'ling.", reply_markup=btn_group)
@dp.message_handler()
async def message_bot(message: types.Message):
    if message.chat.type == "private":
        if message.text == "🔗Do'stlarga ulashish":
            if await check_sub_channels(CHANNELS, message.from_user.id):
                await bot.send_message(message.from_user.id, f"Quyidagi linkni do'stlaringizga ulashish orqali referal to'plang.")
                await bot.send_message(message.from_user.id, f"https://t.me/{BOT_NAME}?start={message.from_user.id}")
            else:
                await bot.send_message(message.from_user.id, "Kechirasiz! Bot to'liq foydalanish uchun kanallarimizga obuna bo'ling.", reply_markup=btn_group)
        if message.text == "👤Profil":
                if await check_sub_channels(CHANNELS, message.from_user.id):
                    await bot.send_message(message.from_user.id, f"Profile - {message.from_user.username}\n\nID raqami: {message.from_user.id}\nReferallar soni: {db.count_referrals(message.from_user.id)}\nHisobingiz: {db.count_referrals(message.from_user.id)*200} so'm", reply_markup=mainMenu)
                else:
                    await bot.send_message(message.from_user.id, "Kechirasiz! Bot to'liq foydalanish uchun kanallarimizga obuna bo'ling.", reply_markup=btn_group)
        if message.text == "📈Reyting":
            if await check_sub_channels(CHANNELS, message.from_user.id):
                ranks = []
                await message.answer("🕔 Iltimos kutib turing...")
                for rank in db.rank():
                    ranks.append(rank[0])
                ranks = [sorted(list(set(ranks)), reverse=True)[0], sorted(list(set(ranks)), reverse=True)[1], sorted(list(set(ranks)), reverse=True)[2]] if len(sorted(list(set(ranks)), reverse=True)) >= 3 else [sorted(list(set(ranks)), reverse=True)[0]]
                ranks = ranks[:2]
                if len(ranks) == 3:
                    await message.answer(f"🥇 {db.get_user(ranks[0])[0]} - {db.count_referrals(ranks[0])} ta\n🥇 {db.get_user(ranks[1])[0]} - {db.count_referrals(ranks[1])} ta\n🥇 {db.get_user(ranks[2])[0]} - {db.count_referrals(ranks[2])} ta")
                if len(ranks) == 2:
                    await message.answer(f"🥇 {db.get_user(ranks[0])[0]} - {db.count_referrals(ranks[0])} ta\n🥇 {db.get_user(ranks[1])[0]} - {db.count_referrals(ranks[1])} ta")
                else:
                    if db.get_user(ranks[0])[0]:
                        await message.answer(f"🥇 {db.get_user(ranks[0])[0]} - {db.count_referrals(ranks[0])} ta")
                    else:
                        await message.answer("...")
            else:
                await bot.send_message(message.from_user.id, "Kechirasiz! Bot to'liq foydalanish uchun kanallarimizga obuna bo'ling.", reply_markup=btn_group)
        if message.text == "📊Statistika":
            if await check_sub_channels(CHANNELS, message.from_user.id):
                await message.answer("🕔 Iltimos kutib turing...")
                stat = len(db.stat())
                await message.answer(f"Bot foydalanuvchiari soni: {stat}")
            else:
                await bot.send_message(message.from_user.id, "Kechirasiz! Bot to'liq foydalanish uchun kanallarimizga obuna bo'ling.", reply_markup=btn_group)
        
        if message.text == "📞Telefon raqamni ulashish":
            if await check_sub_channels(CHANNELS, message.from_user.id):
                await message.answer("🕔 Iltimos kutib turing...")
                stat = len(db.stat())
                await message.answer(f"Bot foydalanuvchiari soni: {stat}")
            else:
                await bot.send_message(message.from_user.id, "Kechirasiz! Bot to'liq foydalanish uchun kanallarimizga obuna bo'ling.", reply_markup=btn_group)
        if message.text == "📝Adminga yozish":
            await message.answer("<a href='t.me/Oltinchipta'>Admin</a>", parse_mode='HTML') 
        if message.text == "📞Raqamni ulashish":
            if not db.get_number(message.from_user.username):
                await PhoneNumber.number.set()
                await message.answer("Telefon raaqamingizni kiriting: ")
            else:
                await message.answer("Raqamingizni qabul qilganmiz.")

@dp.message_handler(lambda message: not is_uzb(message.text), state=PhoneNumber.number)
async def number_invalid(message: types.Message):
    return await message.reply("Raqamingizni to'gri kiriting!")

@dp.message_handler(state=PhoneNumber.number)
async def setNumber(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['number'] = message.text
    db.add_number(data["number"], message.from_user.username)
    await message.answer("✅Telefon raqamingiz saqlandi!")
    await state.finish()
@dp.callback_query_handler(text="subdone")
async def checker(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    if await check_sub_channels(CHANNELS, user_id=message.from_user.id):
        await bot.send_message(message.from_user.id, f"Kanallarimizga obuna bo'lganingiz uchun raxmat. Botimizda foydalanishingiz mumkin.", reply_markup=mainMenu)
    else:
        await bot.send_message(message.from_user.id, "Kechirasiz! Bot to'liq foydalanish uchun kanallarimizga obuna bo'ling.", reply_markup=btn_group)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
