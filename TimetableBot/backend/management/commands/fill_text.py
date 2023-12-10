import asyncio

from django.core.management import BaseCommand
from backend.services.text import fill_text


class Command(BaseCommand):
    help = "Start Telegram user Bot"

    def handle(self, *args, **options):
        fill_text()