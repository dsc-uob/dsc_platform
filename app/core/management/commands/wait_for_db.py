import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('\nWait for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write(
                    self.style.ERROR('Database unavailable! waiting please...')
                )
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available now!'))
