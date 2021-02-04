from django.core.management import BaseCommand

from models.methods import *
import logging
import time
from django.conf import settings
import sys


class Command(BaseCommand):
    def handle(self, *args, **options):
        logging.getLogger().info('Invoked update')
        lockfile = f'analisi_covid_update_{datetime.today().strftime("%Y%m%d")}.lock'
        try:
            if not os.path.exists(lockfile):
                logging.getLogger().info('Starting update')
                updated = False
                while not updated:
                    updated = update_db()
                    if updated:
                        logging.getLogger().info(f'Database updated')
                    else:
                        logging.getLogger().info(
                            f'Database not updated. I will try again in {settings.UPDATE_INTERVAL} seconds')
                        time.sleep(settings.UPDATE_INTERVAL)
                logging.getLogger().info('Update completed')
                if os.path.exists(lockfile):
                    os.remove(lockfile)
        except:
            logging.getLogger().exception(f"Error importing data", exc_info=sys.exc_info())
