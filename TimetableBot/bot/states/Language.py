from aiogram.dispatcher.filters.state import StatesGroup, State


class LanguageState(StatesGroup):
    SELECTING = State()