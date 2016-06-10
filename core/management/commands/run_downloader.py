from django.core.management.base import BaseCommand
from core.downloader import matches


class Command(BaseCommand):

    def handle(self, *args, **options):
        matches.execute_download_games()
