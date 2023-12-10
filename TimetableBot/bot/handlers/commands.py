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

async def new_user(message: types.Message, state: FSMContext):
    telegram_id = message.chat.id
    full_name = message.from_user.full_name
    default_language = ts.get_default_language()
    await message.reply(
        text=get_text(key=td.HELLO_MES, lang=default_language), reply=False
    )
    tus.create_user(telegram_id=telegram_id, full_name=full_name, language=default_language)
    await select_language(message=message, state=state)
    

async def select_language(message: types.Message, state:FSMContext):
    telegram_id = message.chat.id
    data = await state.get_data()
    mes_to_del = data.get("mes_to_del", [])
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    mes = await message.reply(
        text=get_text(key=td.SET_LANGUAGE, lang=user.selected_language),
        reply_markup=await rk.select_language(),
        reply=False
    )
    await message.delete()
    mes_to_del.append(mes.message_id)
    await state.update_data({"mes_to_del":mes_to_del})
    await LanguageState.SELECTING.set()


async def set_language(message: types.Message, state: FSMContext):
    telegram_id = message.chat.id
    data = await state.get_data()
    mes_to_del = data.get("mes_to_del", [])
    selected_language = ts.get_language_by_name(lang_name=message.text)
    tus.update_selected_language(telegram_id=telegram_id, language=selected_language)
    mes_2 = await message.reply(
        text=get_text(key=td.LANGUAGE_SELECTED, lang=selected_language), reply=False
    )
    await MainMenuState.MM.set()
    mes_to_del.append(mes_2.message_id)
    await asyncio.sleep(2)
    await try_delete_message(chat_id=telegram_id, message_id=mes_to_del)
    await main_menu(message=message, state=state)

async def old_user(message: types.Message, state: FSMContext):
    await main_menu(message=message, state=state)


async def back_to_mm(call: types.CallbackQuery, state: FSMContext):
    await main_menu(message=call.message, state=state, back=True)


async def main_menu(message: types.Message, state: FSMContext, back:bool = False):
    telegram_id = message.chat.id
    if not back:
        await message.delete()
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    data = await state.get_data()
    main_message_id = data.get("main_message_id", None)
    await MainMenuState.MM.set()
    await mw.try_edit_message(
        user_id=telegram_id,
        text=get_text(key=td.MAIN_MENU, lang=user.selected_language),
        keyboard=await ik.first_lvl(telegram_id=telegram_id, buttons_list=ld.MAIN_MENU),
        state=state,
    )


async def test(message:types.Message, state: FSMContext):
    print(123)