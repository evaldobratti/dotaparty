from django.core.management.base import BaseCommand
from core.downloader import matches
from core import logger


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--filelog', type=str)
        parser.add_argument('--level', type=str, default='NOTSET')

    def handle(self, *args, **options):
        logger.configure_logger(matches.LOGGER_NAME, options['filelog'], options['level'])
        matches.execute_download_games()
