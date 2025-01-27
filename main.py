import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from db import async_main
from config import TOKEN

from routers.routers import router
from routers.admin_router import admin_router


async def main():
    #await delete_tables()
    #print("База очищена")
    await async_main()
    print("База создана")
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")

