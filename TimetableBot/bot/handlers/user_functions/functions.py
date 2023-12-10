from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.utils.text import get_text
from bot.data import text_data as td
from bot.data import list_data as ld
from backend.services import text as ts
from backend.services import telegram_user as tus
from bot.keyboards import inline as ik
from bot.keyboards import reply as rk
from bot.utils import message_worker as mw
from bot.utils.deleter import try_delete_message
from bot.states.Group import GroupState
from bot.states.MainMenu import MainMenuState
from bot.utils.group_num_validator import group_num_validator
from bot.utils import table_utils as tu


async def update_group(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    await update_group_mess(
        message=call.message, state=state, callback_data=callback_data
    )


async def update_group_mess(
    message: types.Message, state: FSMContext, callback_data: dict
):
    telegram_id = message.chat.id
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    group = user.selected_group or "Не выбрана"
    text = get_text(key=td.CURRENT_GROUP, lang=user.selected_language).format(group)
    keyboard = await ik.second_lvl(
        telegram_id=telegram_id,
        buttons_list=ld.GROUP_UPDATE,
        callback_data=callback_data,
    )
    await mw.try_edit_message(
        user_id=telegram_id, text=text, keyboard=keyboard, state=state
    )


async def check_tt(call: types.CallbackQuery, state: FSMContext, callback_data: dict):
    telegram_id = call.message.chat.id
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    group = user.selected_group or "Не выбрана"
    if group == "Не выбрана":
        await call.answer(text="Сначала выберите группу", show_alert=True, cache_time=5)
        return
    text = tu.get_today_tt(selected_group=user.selected_group)
    keyboard = await ik.weekday(telegram_id=telegram_id, callback_data=callback_data)
    await mw.try_edit_message(
        user_id=telegram_id, text=text, keyboard=keyboard, state=state
    )


async def select_group(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    telegram_id = call.message.chat.id
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    text = get_text(key=td.ENTER_GROUP, lang=user.selected_language)
    keyboard = await ik.third_lvl(
        telegram_id=telegram_id,
        buttons_list=ld.BACK_FROM_UPDATE,
        callback_data=callback_data,
    )
    await GroupState.SELECTING.set()
    await state.update_data({"cd": callback_data})
    await mw.try_edit_message(
        user_id=telegram_id, text=text, keyboard=keyboard, state=state
    )


async def invalid_group(
    message: types.Message, state: FSMContext, callback_data: dict, text=None
):
    telegram_id = message.chat.id
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    if text is None:
        text = get_text(key=td.ENTER_GROUP_ERROR, lang=user.selected_language)
    keyboard = await ik.third_lvl(
        telegram_id=telegram_id,
        buttons_list=ld.BACK_FROM_UPDATE,
        callback_data=callback_data,
    )
    await GroupState.SELECTING.set()
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    await mw.try_send_message(
        user_id=telegram_id, text=text, keyboard=keyboard, state=state
    )
    await try_delete_message(chat_id=telegram_id, message_id=main_message_id)


async def valid_group(message: types.Message, state: FSMContext, groups=list):
    telegram_id = message.chat.id
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    text = get_text(key=td.SELECT_ONE_GROUP, lang=user.selected_language)
    keyboard = await rk.groups(telegram_id=telegram_id, groups_list=groups)
    await GroupState.ONE_OF.set()
    data = await state.get_data()
    main_message_id = data.get("main_message_id")
    await mw.try_send_message(
        user_id=telegram_id, text=text, keyboard=keyboard, state=state
    )
    await try_delete_message(chat_id=telegram_id, message_id=main_message_id)


async def first_lvl_functions_splitter(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    action = callback_data["action"]
    await MainMenuState.MM.set()
    await splitter[action](call=call, state=state, callback_data=callback_data)


async def second_lvl_functions_splitter(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    action = callback_data["action_2"]
    await MainMenuState.MM.set()
    await splitter[action](call=call, state=state, callback_data=callback_data)


async def third_lvl_functions_splitter(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    action = callback_data["action_2"]
    if callback_data["action_3"] == td.BACK:
        action = callback_data["action"]
    await splitter[action](call=call, state=state, callback_data=callback_data)


splitter = {
    td.UPDATE_GROUP_NUM: update_group,
    td.CHECK_TT: check_tt,
    td.SELECT_GROUP: select_group,
}


async def get_group_num(message: types.Message, state: FSMContext):
    group_num = message.text
    valid = group_num_validator(user_input=group_num)
    data = await state.get_data()
    if valid:
        group_num = tu.get_group_num(user_input=group_num)
        df = tu.get_main_df()
        group_names = tu.get_cleaned_group_names(df=df)
        groups_dict = tu.get_groups_dict_by_group_numbers(
            df=df, cleaned_group_names=group_names
        )
        try:
            group_names = tu.get_founded_group_names(
                user_input=group_num, groups_dict=groups_dict
            )
            await valid_group(message=message, state=state, groups=group_names)
        except (tu.GroupNotFound, tu.NotGroupNumStyle) as e:
            print(e.get_message())
            await invalid_group(
                message=message,
                state=state,
                callback_data=data["cd"],
                text=e.get_message(),
            )
    else:
        await invalid_group(message=message, state=state, callback_data=data["cd"])


async def set_group(message: types.Message, state: FSMContext):
    group = message.text
    telegram_id = message.chat.id
    data = await state.get_data()
    cd = data.get("cd")
    tus.update_selected_group(telegram_id=telegram_id, group=group)
    await try_delete_message(
        chat_id=telegram_id, message_id=data.get("main_message_id")
    )
    await update_group_mess(message=message, state=state, callback_data=cd)


async def select_is_odd(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    telegram_id = call.message.chat.id
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    text = get_text(key=td.IS_ODD, lang=user.selected_language).format(
        tu.get_today_is_odd_txt()
    )
    keyboard = await ik.weekday_selected(
        telegram_id=telegram_id, callback_data=callback_data
    )
    await mw.try_edit_message(
        user_id=telegram_id, text=text, keyboard=keyboard, state=state
    )


async def check_tt_by_data(
    call: types.CallbackQuery, state: FSMContext, callback_data: dict
):
    telegram_id = call.message.chat.id
    user = tus.get_profile_by_telegram_id(telegram_id=telegram_id)
    day = callback_data["day"]
    is_odd = int(callback_data["is_odd"])
    text = text = tu.get_tt(
        selected_group=user.selected_group, selected_weekday=day, is_odd=is_odd
    )
    keyboard = await ik.is_odd_selected(
        telegram_id=telegram_id, callback_data=callback_data
    )
    await mw.try_edit_message(
        user_id=telegram_id, text=text, keyboard=keyboard, state=state
    )
