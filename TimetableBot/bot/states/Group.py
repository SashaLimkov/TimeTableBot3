from aiogram.dispatcher.filters.state import StatesGroup, State


class GroupState(StatesGroup):
    SELECTING = State()
    ONE_OF = State()
