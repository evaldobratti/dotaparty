from django.core.management.base import BaseCommand
from core.parameters import INTERESTED_ACCOUNTS_IDS
from core.tasks import download_games
from core.models import Account


class Command(BaseCommand):

    def handle(self, *args, **options):
        for account_id in INTERESTED_ACCOUNTS_IDS.value():
            a = Account.objects.get(account_id=account_id)
            download_games(a)
