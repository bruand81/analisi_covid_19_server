from django.core.management import BaseCommand

from models.methods import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        csv_to_db_regioni()
        csv_to_db_province()