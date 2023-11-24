import asyncio

from django.core.management import BaseCommand

from bot.app import run_bot


class Command(BaseCommand):
    help = "Start Telegram user Bot"

    def handle(self, *args, **options):
        asyncio.run(run_bot())