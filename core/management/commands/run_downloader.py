from django.core.management.base import BaseCommand
from core.parameters import LAST_MATCH_SEQ_NUM
from core.downloader import matches


class Command(BaseCommand):

    def handle(self, *args, **options):
        LAST_MATCH_SEQ_NUM.reset()
        matches.execute_download_games()
