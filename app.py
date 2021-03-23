import logging
import middlewares

from apps import dispatcher, admin
from aiogram import executor


async def on_startup(dispatcher):
    middlewares.setup(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dispatcher, on_startup=on_startup)

