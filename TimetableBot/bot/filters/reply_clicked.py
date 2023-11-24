from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from backend.services.text import get_key_by_text
from bot.data import list_data as ld

class InMainKB(BoundFilter):
    async def check(self, message: types.Message | types.CallbackQuery) -> bool:
        match type(message):
            case types.Message:
                text = message.text
                key = get_key_by_text(text=text)
                return key in ld.SELECTED_MENU.keys()
            case _:
                return False