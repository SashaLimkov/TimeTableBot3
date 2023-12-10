from bot.utils.text import get_text
from bot.utils.base_keyboard_utils import get_base_keyboard, get_inline_button
from backend.services import telegram_user as tus
from bot.data import text_data as td
from bot.data import list_data as ld
from bot.data import callback_data as cd


__all__ = [
    "back_to_mm",
    "first_lvl",
    "second_lvl",
    "third_lvl",
    "weekday",
    "weekday_selected",
    "is_odd_selected"
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


async def first_lvl(telegram_id, buttons_list: tuple|None):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    if not buttons_list is None:
        for key in buttons_list:
            if key == td.TURN_OFF_ON_NOTIFICATIONS:
                keyboard.add(
                    await get_inline_button(
                        text=get_text(key=key, lang=user.selected_language).format("✅" if user.notifications else "❌"),
                        cd=key
                    )
                )
                continue
            keyboard.add(
                await get_inline_button(
                    text=get_text(key=key, lang=user.selected_language),
                    cd=cd.LVL_1.new(
                        action=key
                    )
                )
            )
    return keyboard

async def second_lvl(telegram_id, buttons_list: tuple|None, callback_data:dict):
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
                    cd=cd.LVL_2.new(
                        action=callback_data["action"],
                        action_2=key
                    )
                )
            )
    keyboard.add(
        await get_inline_button(
                    text=get_text(key=td.BACK_TO_MM, lang=user.selected_language),
                    cd=td.BACK_TO_MM
                )
    )
    return keyboard

async def third_lvl(telegram_id, buttons_list: tuple|None, callback_data:dict):
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
                    cd=cd.LVL_3.new(
                        action=callback_data["action"],
                        action_2=callback_data["action_2"],
                        action_3=key
                    )
                )
            )
    return keyboard

async def weekday(telegram_id, callback_data:dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 2,
        },
    )
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    for key in ld.WEEKDAY_NAMES:
        keyboard.insert(
            await get_inline_button(
                text=key,
                cd=cd.WEEKDAY.new(
                    action=callback_data["action"],
                    day=key
                )
            )
        )
    keyboard.add(
        await get_inline_button(
                    text=get_text(key=td.BACK_TO_MM, lang=user.selected_language),
                    cd=td.BACK_TO_MM
                )
    )
    return keyboard


async def weekday_selected(telegram_id, callback_data:dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    for key in ["Четная", "Нечетная"]:
        keyboard.add(
            await get_inline_button(
                text=key,
                cd=cd.WEEKDAY_OE.new(
                    action=callback_data["action"],
                    day=callback_data["day"],
                    is_odd=0 if key == "Четная" else 1
                )
            )
        )
    keyboard.add(
                await get_inline_button(
                    text=get_text(key=td.BACK, lang=user.selected_language),
                    cd=cd.LVL_1.new(
                        action=callback_data["action"],
                    )
                )
            )
    return keyboard


async def is_odd_selected(telegram_id, callback_data:dict):
    keyboard = await get_base_keyboard(
        keyboard_options={
            "row_width": 1,
        },
    )
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    keyboard.add(
                await get_inline_button(
                    text=get_text(key=td.BACK, lang=user.selected_language),
                    cd=cd.WEEKDAY.new(
                        action=callback_data["action"],
                        day=callback_data["day"]
                    )
                )
            )
    return keyboard