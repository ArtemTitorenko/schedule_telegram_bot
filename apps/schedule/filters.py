import re

from aiogram.dispatcher.filters import Command
from aiogram import types
from typing import Union, Iterable


class CommandWithArg(Command):

    def __init__(self,
                 commands: Union[Iterable, str],
                 pattern: str,
                 *args, **kwargs) -> None:

        super().__init__(commands, *args, **kwargs)
        self._pattern = pattern


    async def check(self, message: types.Message) -> bool:
        is_command = await super().check(message)
        args = message.get_args()
        if is_command and len(args) > 0 and re.fullmatch(self._pattern, args):
            return True
        return False

