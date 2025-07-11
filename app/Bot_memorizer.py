import asyncio
import logging
import sys
import os 

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN").strip()

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import hendlers_start_db, hendlers_clear, hendlers_credo
dp = Dispatcher()

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(hendlers_start_db.router)
    dp.include_routers(hendlers_clear.router)
    dp.include_routers(hendlers_credo.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    
