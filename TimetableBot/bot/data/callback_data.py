from aiogram.utils.callback_data import CallbackData

IN_DEV = "in_dev"


LVL_1 = CallbackData("lvl_1", "action")
LVL_2 = CallbackData("lvl_2", "action", "action_2")
WEEKDAY = CallbackData("wd", "action", "day")
WEEKDAY_OE = CallbackData("wdoe", "action", "day", "is_odd")
LVL_3 = CallbackData("lvl_3", "action", "action_2", "action_3")