from aiogram import Dispatcher
from aiogram.dispatcher import filters

from bot.filters.not_registered import NotRegistered
from bot.states.Group import GroupState
from bot.data import text_data as td
from bot.data import list_data as ld
from bot.data import callback_data as cd
from aiogram import types
# from bot.data import callback_data as cd
from . import settings, functions

def setup(dp: Dispatcher):
    dp.register_callback_query_handler(
        settings.switch_notifications,
        filters.Text(td.TURN_OFF_ON_NOTIFICATIONS),
        state="*"
    )
    dp.register_callback_query_handler(
        functions.first_lvl_functions_splitter,
        cd.LVL_1.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        functions.second_lvl_functions_splitter,
        cd.LVL_2.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        functions.third_lvl_functions_splitter,
        cd.LVL_3.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        functions.select_is_odd,
        cd.WEEKDAY.filter(),
        state="*"
    )
    dp.register_callback_query_handler(
        functions.check_tt_by_data,
        cd.WEEKDAY_OE.filter(),
        state="*"
    )
    dp.register_message_handler(
        functions.get_group_num,
        state=GroupState.SELECTING,
    )
    dp.register_message_handler(
        functions.set_group,
        state=GroupState.ONE_OF,
    )
