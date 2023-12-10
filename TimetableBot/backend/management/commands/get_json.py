import asyncio

from django.core.management import BaseCommand
from backend.services.text import create_data_json


class Command(BaseCommand):
    help = "Start Telegram user Bot"

    def handle(self, *args, **options):
        create_data_json()