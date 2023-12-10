from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.utils.text import get_text
from bot.data import text_data as td
from bot.data import list_data as ld
from backend.services import text as ts
from backend.services import telegram_user as tus
from bot.keyboards import inline as ik
from bot.utils import message_worker as mw
from bot.utils.deleter import try_delete_message


async def switch_notifications(call: types.CallbackQuery, state=FSMContext):
    telegram_id = call.message.chat.id
    data = await state.get_data()
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    tus.switch_notifications(telegram_id=telegram_id)
    key = td.OFF_NTF if user.notifications else td.ON_NTF
    text = get_text(key=key, lang=user.selected_language)
    await call.answer(
        text=text,
        show_alert=True,
        cache_time=5,
    )
    await mw.try_edit_keyboard(
        chat_id=telegram_id,
        message_id=data.get("main_message_id"),
        keyboard=await ik.first_lvl(telegram_id=telegram_id, buttons_list=ld.MAIN_MENU),
    )
