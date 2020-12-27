from django.core.management import BaseCommand

from models.methods import *
import logging
import time
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.getLogger().info('Invoked update')
        lock_file = f'analisi_covid_update_{datetime.today().strftime("%Y%m%d")}.lock'
        if not os.path.exists(lock_file):
            logging.getLogger().info('Starting update')
            updated = False
            while not updated:
                updated = update_db()
                if updated:
                    logging.getLogger().info(f'Database updated')
                else:
                    logging.getLogger().info(f'Database not updated. I will try again in {settings.UPDATE_INTERVAL} seconds')
                    time.sleep(settings.UPDATE_INTERVAL)
            logging.getLogger().info('Update completed')
            if os.path.exists(lock_file):
                os.remove(lock_file)
