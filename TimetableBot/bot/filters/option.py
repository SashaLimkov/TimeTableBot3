from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from backend.services.text import get_key_by_text
from bot.data import list_data as ld

class SelectedOption(BoundFilter):
    async def check(self, message: types.Message | types.CallbackQuery) -> bool:
        match type(message):
            case types.CallbackQuery:
                cd = message.data
                return cd in ld.SELECTED_OPTION.keys()
            case _:
                return False