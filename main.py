import asyncio
import logging
import sys

import aiogram
from aiogram import Bot, Dispatcher
from db import async_main, delete_tables
from config import TOKEN
from requests import clear_table
from routers import router


async def main():
    #await delete_tables()
    #print("База очищена")
    await async_main()
    print("База создана")
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

