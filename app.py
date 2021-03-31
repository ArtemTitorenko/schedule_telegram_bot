import logging
import middlewares

from apps import dp
from aiogram import executor
from database import init_connection


async def on_startup(dp):
    middlewares.setup(dp)
    await init_connection()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

