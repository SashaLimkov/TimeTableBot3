from aiogram import Dispatcher
from aiogram.dispatcher import filters
from bot.filters.option import SelectedOption
from bot.filters.reply_clicked import InMainKB

from bot.filters.not_registered import NotRegistered
from bot.states.Language import LanguageState
from bot.data import text_data as td
from bot.data import list_data as ld
from aiogram import types
# from bot.data import callback_data as cd
from . import commands, reply_splitter

def setup(dp: Dispatcher):
    dp.register_message_handler(
        commands.new_user,
        filters.CommandStart(),
        NotRegistered(),
        state="*",
    )

    dp.register_message_handler(
        commands.old_user,
        filters.CommandStart(),
        state="*",
    )

    dp.register_message_handler(
        commands.select_language,
        filters.Command("language"),
        state="*",
    )

    dp.register_message_handler(
        commands.set_language,
        state=LanguageState.SELECTING,
    )

    dp.register_callback_query_handler(
        commands.back_to_mm,
        filters.Text(td.BACK_TO_MM),
        state="*"
    )
    dp.register_callback_query_handler(
        reply_splitter.get_message_by_selcted_option,
        SelectedOption(),
        state="*"
    )
    # dp.register_message_handler(
    #     commands.test,
    #     state="*"
    # )
    dp.register_message_handler(
        reply_splitter.get_func_by_reply_selection,
        InMainKB(),
        state="*"
    )
    dp.register_callback_query_handler(
        reply_splitter.in_dev,
        state="*"
    )