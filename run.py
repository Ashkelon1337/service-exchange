import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from database.models import init_db
from bot.handlers.start import router as r1
from bot.handlers.client import router as r2
from bot.handlers.orders import router as r3
from bot.handlers.executor import router as r4
from bot.handlers.admin import router as r5

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(r1, r2, r3, r4, r5)

async def main():
    await init_db()
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')