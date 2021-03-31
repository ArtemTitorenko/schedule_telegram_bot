import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

from typing import Union, Optional

from loader import dp

from .services import get_group_week_schedule_by_group_code, \
        get_user_week_schedule
from .filters import CommandWithArg


GROUP_CODE_PATTERN = r'[А-Яа-я]{1,}\-\d{2,}\-\d{2,}'
@dp.message_handler(CommandWithArg('schedule', GROUP_CODE_PATTERN))
async def group_week_schedule_handler(message: types.Message):
    group_code = message.get_args()
    date = datetime.date.today()
    week_schedule = await get_group_week_schedule_by_group_code(
            group_code, date)
    await message.answer(week_schedule.week.type)


@dp.message_handler(Command('schedule'))
async def user_week_scedule_handler(message: types.Message):
    user_telegram_id = message.from_user.id
    date = datetime.date.today()
    week_schedule = await get_user_week_schedule(user_telegram_id, date)
    if not week_schedule:
        await message.answer('Нужно ввести группу')
        return
    await message.answer(week_schedule.week.type)

