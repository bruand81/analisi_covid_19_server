from django.core.management import BaseCommand

from models.methods import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        clean_region_from_db()
        clean_province_from_db()
        csv_to_db_regioni()
        csv_to_db_province()