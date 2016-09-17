from django.core.management.base import BaseCommand
from ...models import Proxy
class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        with open(options['file'][0]) as f:
            for l in f:
                address = str(l).strip()
                print 'importando: ' + address
                Proxy.objects.create(address=address)
        print 'done'
