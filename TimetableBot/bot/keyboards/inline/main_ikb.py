from bot.utils.text import get_text
from bot.utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from backend.services import telegram_user as tus
from bot.data import text_data as td
from bot.data import list_data as ld


__all__ = [
    "back_to_mm",
    "selected_menu"
]

async def back_to_mm(telegram_id):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    keyboard.add(
        await get_inline_button(
            text=get_text(key=td.BACK_TO_MM, lang=user.selected_language),
            cd=td.BACK_TO_MM
        )
    )
    return keyboard


async def selected_menu(telegram_id, buttons_list: list|None):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    if not buttons_list is None:
        for key in buttons_list:
            keyboard.add(
                await get_inline_button(
                    text=get_text(key=key, lang=user.selected_language),
                    cd=key
                )
            )
    keyboard.add(
        await get_inline_button(
                text=get_text(key=td.BACK_TO_MM, lang=user.selected_language),
                cd=td.BACK_TO_MM
            )
    )
    return keyboard
