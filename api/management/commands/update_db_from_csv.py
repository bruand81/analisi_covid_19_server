from django.core.management import BaseCommand

from models.methods import update_db


class Command(BaseCommand):
    def handle(self, *args, **options):
        update_db()
