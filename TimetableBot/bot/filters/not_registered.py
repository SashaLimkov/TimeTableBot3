from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from backend.services import telegram_user


class NotRegistered(BoundFilter):
    async def check(self, message: types.Message | types.CallbackQuery) -> bool:
        match type(message):
            case types.Message:
                user_id = message.from_user.id
                user_profile = telegram_user.get_profile_by_telegram_id(user_id)
                return True if not user_profile else False
            case types.CallbackQuery:
                user_id = message.message.from_user.id
                user_profile = telegram_user.get_profile_by_telegram_id(user_id)
                return True if not user_profile else False
            case _:
                return False