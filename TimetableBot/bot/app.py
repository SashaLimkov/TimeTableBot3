from aiogram import Dispatcher
from aiogram.utils import executor

from .config.loader import dp, scheduler
from . import filters, handlers

import os
import django
import datetime


def scheduler_func():
    scheduler.add_job(notifier, "cron", day_of_week="mon-sun", hour=8)


def run_bot():
    """Запускает процессы бота"""
    _setup_django()
    print("Bot started")
    executor.start_polling(
        dp, on_startup=_on_startup, on_shutdown=_on_shutdown, skip_updates=False
    )


async def _on_startup(dispatcher: Dispatcher):
    """Регистрирует ветки handlers"""
    handlers.setup(dispatcher)
    # scheduler_func()


async def _on_shutdown(dispatcher: Dispatcher):
    """Ожидает и закрывает хранилище dispatcher"""
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


def _setup_django():
    """Установка окружения Django внутри бота"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()