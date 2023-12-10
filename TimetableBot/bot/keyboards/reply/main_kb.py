from bot.utils.text import get_text
from backend.services import text as ts
from backend.services import telegram_user as tus
from bot.data import list_data as ls
from bot.utils.base_keyboard_utils import get_base_keyboard, get_keyboard_button

__all__ = [
    "select_language",
    "main_menu",
    "groups"
]


async def select_language():
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
            "resize_keyboard": True,
            "one_time_keyboard":True
        },
        is_inline=False
    )
    for language in ts.get_all_languages():
        keyboard.add(
            await get_keyboard_button(
                button={"text": language.name,},
                is_inline=False
            )
        )
    return keyboard

async def main_menu(telegram_id):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 2,
            "resize_keyboard": True,
            "one_time_keyboard":False
        },
        is_inline=False
    )
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    for key in []:
        keyboard.insert(
            await get_keyboard_button(
                button={"text": get_text(key=key, lang=user.selected_language),},
                is_inline=False
            )
        )
    return keyboard

async def groups(telegram_id, groups_list):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
            "resize_keyboard": True,
            "one_time_keyboard":True
        },
        is_inline=False
    )
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    for key in groups_list:
        keyboard.add(
            await get_keyboard_button(
                button={"text": key,},
                is_inline=False
            )
        )
    return keyboard