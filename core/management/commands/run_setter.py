from django.core.management.base import BaseCommand
from core.downloader import skill_setter
from core import logger


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--logfile', type=str, default='')
        parser.add_argument('--level', type=str, default='DEBUG')

    def handle(self, *args, **options):
        if options['logfile']:
            logger.configure_logger(skill_setter.LOGGER_NAME, options['logfile'], options['level'])
        skill_setter.execute_skill_setter()