from django.core.management.base import BaseCommand
from core.downloader.skill_setter import execute_skill_setter


class Command(BaseCommand):
    def handle(self, *args, **options):
        execute_skill_setter()
