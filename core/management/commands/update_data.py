from django.core.management.base import BaseCommand
from core.utils import update_heroes
from core.utils import update_items


class Command(BaseCommand):

    def handle(self, *args, **options):
        update_heroes()
        update_items()
