from django.core.management.base import BaseCommand
from core.downloader.matches import execute_download_games


class Command(BaseCommand):
    def handle(self, *args, **options):
        execute_download_games()
