import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from bot.states.MainMenu import MainMenuState
from bot.states.Language import LanguageState

from bot.utils.text import get_text
from bot.data import text_data as td
from bot.data import list_data as ld
from backend.services import text as ts
from backend.services import telegram_user as tus
from bot.keyboards import reply as rk
from bot.keyboards import inline as ik
from bot.utils import message_worker as mw
from bot.utils.deleter import try_delete_message


async def get_func_by_reply_selection(message: types.Message, state:FSMContext):
    text_key = ts.get_key_by_text(text=message.text)
    data = await state.get_data()
    telegram_id = message.chat.id
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    main_message_id = data.get("main_message_id")
    answer = get_text(key=td.SELECT, lang=user.selected_language)
    keyboard = await ik.selected_menu(telegram_id=telegram_id, buttons_list=ld.SELECTED_MENU[text_key])
    await try_delete_message(chat_id=telegram_id, message_id=main_message_id)
    await mw.try_send_message(
        user_id=telegram_id,
        text=answer,
        keyboard=keyboard,
        state=state
    )

async def get_message_by_selcted_option(call: types.CallbackQuery, state:FSMContext):
    cd = call.data
    text_key, buttons_list = ld.SELECTED_OPTION[cd]
    data = await state.get_data()
    telegram_id = call.message.chat.id
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    main_message_id = data.get("main_message_id")
    answer = get_text(key=text_key, lang=user.selected_language)
    keyboard = await ik.selected_menu(telegram_id=telegram_id, buttons_list=buttons_list)
    await try_delete_message(chat_id=telegram_id, message_id=main_message_id)
    await mw.try_send_message(
        user_id=telegram_id,
        text=answer,
        keyboard=keyboard,
        state=state
    )

async def in_dev(call:types.CallbackQuery, state:FSMContext):
    await call.answer(text="В разработке", show_alert=True)