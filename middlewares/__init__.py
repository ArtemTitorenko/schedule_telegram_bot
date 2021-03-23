from aiogram import Dispatcher

from loader import dispatcher
from .throttling import ThrottlingMiddleware


def setup(dispatcher: Dispatcher):
    dispatcher.middleware.setup(ThrottlingMiddleware())

