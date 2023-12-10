import datetime
from backend.models.TelegramUser import TelegramUser

from bot.config.loader import bot
from bot.data import text_data as td
from bot.utils import table_utils as tu


async def notifier():
    users = TelegramUser.objects.filter(notifications=True).all()
    for user in users:
        text = tu.get_today_tt(
            selected_group=user.selected_group
        )
        await bot.send_message(
            chat_id=user.telegram_id,
            text=text
        )