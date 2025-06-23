
import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters import BaseFilter

TOKEN = "8172034278:AAFMDdinPV7WIkJ6da_hwPOXH_GWk03UNwE"
ALLOWED_USER_ID = 1958499426

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Фильтр на пользователя
class IsOwner(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == ALLOWED_USER_ID

@dp.message(Command("start"), IsOwner())
async def cmd_start(message: Message):
    await message.answer("👋 Вітаю! Надішли номер ТТН Укрпошти, і я скажу статус відправлення.")

async def track_ukrposhta(ttn: str):
    url = "https://track.ukrposhta.ua/tracking/api/v1/track"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    json_data = {
        "barcode": ttn,
        "language": "UA"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=json_data) as response:
            try:
                data = await response.json()
                status = data['lastStatus']['status']
                date = data['lastStatus']['date']
                index = data['lastStatus']['index']
                return f"<b>📦 Статус:</b> {status}\n<b>📅 Дата:</b> {date}\n<b>📮 Відділення:</b> {index}"
            except:
                return "❗ Не вдалося отримати дані. Перевір ТТН або спробуй пізніше."

@dp.message(IsOwner())
async def handle_ttn(message: Message):
    ttn = message.text.strip()
    if not ttn.isdigit() or len(ttn) < 13:
        await message.answer("⚠️ Введи коректний номер ТТН (13 цифр).")
        return
    await message.answer("🔍 Перевіряю статус...")
    result = await track_ukrposhta(ttn)
    await message.answer(result)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
