import asyncio
from pathlib import Path
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from TimetableBot import settings
from apscheduler.schedulers.asyncio import AsyncIOScheduler

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML", disable_web_page_preview=True)
storage = JSONStorage(f'{Path.cwd()}/{"fsm_data2.json"}')
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=storage, loop=loop)
scheduler = AsyncIOScheduler()
