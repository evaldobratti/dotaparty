from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from core.tasks import games_skill_setter
        games_skill_setter()
