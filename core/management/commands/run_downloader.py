from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        from core.tasks import download_by_seq_num
        download_by_seq_num()
