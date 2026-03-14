import os
import logging
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN

# Импортируем твоё FastAPI приложение и функцию инициализации БД
from api.main import app as fastapi_app
from database.models import init_db

# Твои роутеры бота
from bot.handlers.start import router as r1
from bot.handlers.client import router as r2
from bot.handlers.orders import router as r3
from bot.handlers.executor import router as r4
from bot.handlers.admin import router as r5

RENDER_URL = os.getenv("RENDER_EXTERNAL_URL")
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"{RENDER_URL}{WEBHOOK_PATH}"

logging.basicConfig(level=logging.INFO)

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
dp.include_routers(r1, r2, r3, r4, r5)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logging.info("Initializing database...")
    await init_db()

    # 2. Регистрируем вебхук в Telegram
    logging.info(f"Setting webhook to: {WEBHOOK_URL}")
    await bot.set_webhook(
        url=WEBHOOK_URL,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )

    yield

    await bot.session.close()
    logging.info("Server shutting down...")


fastapi_app.router.lifespan_context = lifespan


@fastapi_app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    port = int(os.getenv("PORT", 8000))

    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)
