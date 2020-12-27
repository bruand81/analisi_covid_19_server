import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction

from models.DatiProvince import DatiProvince
from models.DatiRecenti import DatiRecenti
from models.DatiRegioni import DatiRegioni
from models.utils import convert_to_datetime
from province.models import ProvinceItaliane
from regioni.models import RegioniItaliane
import os
from datetime import datetime

lock_file = f'analisi_covid_update_{datetime.today().strftime("%Y%m%d")}.lock'


def update_db():
    latest_date_online = DatiRecenti().last_update_date
    updated = False
    if not os.path.exists(lock_file):
        logging.getLogger().info('Check if update db is needed')
        logging.getLogger().info(f'Last online version of data is: {latest_date_online.strftime("%x")}')
        count_regioni = 0
        count_province = 0

        if RegioniItaliane.objects.exists():
            latest_date_in_db = RegioniItaliane.objects.latest('data').data
            logging.getLogger().info(f'Last last version in region DB: {latest_date_in_db.strftime("%x")}')
            if (latest_date_online - latest_date_in_db).days > 0:
                count_regioni += csv_to_db_regioni()
                updated = True
            else:
                if RegioniItaliane.objects.filter(data=latest_date_in_db).count() < 20:
                    count_regioni += csv_to_db_regioni()
                    updated = True
                else:
                    logging.getLogger().info('Region update not needed')
        else:
            count_regioni += csv_to_db_regioni()
            updated = True

        if ProvinceItaliane.objects.exists():
            latest_date_in_db = ProvinceItaliane.objects.latest('data').data
            latest_date_province = latest_date_in_db
            logging.getLogger().info(f'Last last version in county DB: {latest_date_in_db.strftime("%x")}')
            if (latest_date_online - latest_date_in_db).days > 0:
                count_province += csv_to_db_province()
                updated = True
            else:
                if ProvinceItaliane.objects.filter(data=latest_date_in_db).count() < 20:
                    count_province += csv_to_db_province()
                    updated = True
                else:
                    logging.getLogger().info('Province update not needed')
        else:
            count_province += csv_to_db_province()
            updated = True

        if updated:
            os.remove(lock_file)
            logging.getLogger().info(f'update.lock removed')
            logging.getLogger().info(f'{__name__}: Database updated')
            subject = f'Aggiornamento dati COVID 19 Italia [{latest_date_online.strftime("%c")}]'
            message = f'Database dell\'app Covid 19 Italia aggiornato al {latest_date_online.strftime("%c")}' \
                           f'Collegati all\'indirizzo https://antarescloud.antaresnet.org/www' \
                           f'sono stati aggiornati/aggiunti {count_regioni} dati regionali/nazionali e {count_province}  dati provinciali'
            message_html = f'<p>Database dell\'app Covid 19 Italia aggiornato al <strong>{latest_date_online.strftime("%c")}</strong></p>' \
                      f'<p>Collegati all\'indirizzo <a href="https://antarescloud.antaresnet.org/www">' \
                      f'https://antarescloud.antaresnet.org/www</a></p>'\
                      f'<p>sono stati aggiornati/aggiunti <strong>{count_regioni}</strong> dati regionali/nazionali e <strong>{count_province}</strong>  dati provinciali</p>'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ['andrea.bruno@antaresnet.org', ]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False, html_message=message_html)
        else:
            logging.getLogger().info(f'{__name__}: Database not updated')
    else:
        logging.getLogger().info(f'Lock file exists. Skipping update {os.path.abspath(lock_file)}')
        # print(f'Lock file exists. Skypping update')

    return updated


def csv_to_db():
    csv_to_db_regioni()
    csv_to_db_province()


def csv_to_db_province() -> int:
    open(lock_file, 'a').close()
    logging.getLogger().info(f'update.lock created')
    df = DatiProvince().dati_provinciali
    records = df.to_records()  # convert to records

    logging.getLogger().info("Saving county in DB")
    count = 0
    with transaction.atomic():
        for record in records:
            dato_provinciale = ProvinceItaliane(
                index=record.index,
                data=convert_to_datetime(record.date),
                codice_regione=record.codice_regione,
                denominazione_regione=record.denominazione_regione,
                codice_provincia=record.codice_provincia,
                denominazione_provincia=record.denominazione_provincia,
                lat=record.lat,
                long=record.long,
                sigla_provincia=record.sigla_provincia,
                totale_casi=record.totale_casi,
                incidenza=record.incidenza,
                variazione_totale_casi=record.variazione_totale_casi,
                percentuale_variazione_totale_casi=record.percentuale_variazione_totale_casi,
                variazione_totale_casi_3dma=record.variazione_totale_casi_3dma,
                variazione_totale_casi_7dma=record.variazione_totale_casi_7dma,
                incidenza_7d=record.incidenza_7d,
                nuovi_positivi_7dsum=record.nuovi_positivi_7dsum,
                nuovi_positivi_7d_incr=record.nuovi_positivi_7d_incr
            )
            dato_provinciale.save()
            count += 1
    logging.getLogger().info("County data saved in DB")
    return count


def csv_to_db_regioni() -> int:
    open(lock_file, 'a').close()
    logging.getLogger().info(f'update.lock created')
    df = DatiRegioni().dati_completi
    records = df.to_records()  # convert to records

    logging.getLogger().info("Saving region in DB")
    count = 0
    with transaction.atomic():
        for record in records:
            # ts = (record.date - np.datetime64('1970-01-01T00:00:00Z')) / np.timedelta64(1, 's')
            # record_date = datetime.utcfromtimestamp(ts)
            dato_regionale = RegioniItaliane(
                index=record.index,  # index
                # data=record_date,  # 72
                data=convert_to_datetime(record.date),
                codice_regione=record.codice_regione,  # 18
                denominazione_regione=record.denominazione_regione,  # 19
                lat=record.lat,  # 20
                long=record.long,  # 21

                # Direct source data
                ricoverati_con_sintomi=record.ricoverati_con_sintomi,  # 3
                terapia_intensiva=record.terapia_intensiva,  # 4
                totale_ospedalizzati=record.totale_ospedalizzati,  # 5
                isolamento_domiciliare=record.isolamento_domiciliare,  # 6
                totale_positivi=record.totale_positivi,  # 7
                variazione_totale_positivi=record.variazione_totale_positivi,  # 8
                nuovi_positivi=record.nuovi_positivi,  # 9
                dimessi_guariti=record.dimessi_guariti,  # 10
                deceduti=record.deceduti,  # 11
                casi_da_sospetto_diagnostico=record.casi_da_sospetto_diagnostico,  # 12
                casi_da_screening=record.casi_da_screening,  # 13
                totale_casi=record.totale_casi,  # 14
                tamponi=record.tamponi,  # 15
                casi_testati=record.casi_testati,  # 16
                popolazione=record.popolazione,  # 22
                incidenza=record.incidenza,  # 23

                # Daily variation data
                variazione_casi_da_screening=record.variazione_casi_da_screening,  # 25
                variazione_casi_da_sospetto_diagnostico=record.variazione_casi_da_sospetto_diagnostico,  # 26
                variazione_casi_testati=record.variazione_casi_testati,  # 27
                variazione_deceduti=record.variazione_deceduti,  # 28
                variazione_dimessi_guariti=record.variazione_dimessi_guariti,  # 29
                variazione_isolamento_domiciliare=record.variazione_isolamento_domiciliare,  # 30
                variazione_ricoverati_con_sintomi=record.variazione_ricoverati_con_sintomi,  # 31
                variazione_tamponi=record.variazione_tamponi,  # 32
                variazione_terapia_intensiva=record.variazione_terapia_intensiva,  # 33
                percentuale_variazione_casi_da_screening=record.percentuale_variazione_casi_da_screening,  # 35
                percentuale_variazione_casi_da_sospetto_diagnostico=record.percentuale_variazione_casi_da_sospetto_diagnostico,
                # 36
                percentuale_variazione_casi_testati=record.percentuale_variazione_casi_testati,  # 37
                percentuale_variazione_deceduti=record.percentuale_variazione_deceduti,  # 38
                percentuale_variazione_dimessi_guariti=record.percentuale_variazione_dimessi_guariti,  # 39
                percentuale_variazione_isolamento_domiciliare=record.percentuale_variazione_isolamento_domiciliare,
                # 40
                percentuale_variazione_ricoverati_con_sintomi=record.percentuale_variazione_ricoverati_con_sintomi,
                # 41
                percentuale_variazione_tamponi=record.percentuale_variazione_tamponi,  # 42
                percentuale_variazione_terapia_intensiva=record.percentuale_variazione_terapia_intensiva,  # 43
                percentuale_positivi_casi_7dma=record.percentuale_positivi_casi_7dma,
                percentuale_positivi_casi_3dma=record.percentuale_positivi_casi_3dma,

                # 3DMA variation data
                variazione_casi_da_screening_3dma=record.variazione_casi_da_screening_3dma,  # 45
                variazione_casi_da_sospetto_diagnostico_3dma=record.variazione_casi_da_sospetto_diagnostico_3dma,  # 46
                variazione_casi_testati_3dma=record.variazione_casi_testati_3dma,  # 47
                variazione_deceduti_3dma=record.variazione_deceduti_3dma,  # 48
                variazione_dimessi_guariti_3dma=record.variazione_dimessi_guariti_3dma,  # 49
                variazione_isolamento_domiciliare_3dma=record.variazione_isolamento_domiciliare_3dma,  # 50
                variazione_ricoverati_con_sintomi_3dma=record.variazione_ricoverati_con_sintomi_3dma,  # 51
                variazione_tamponi_3dma=record.variazione_tamponi_3dma,  # 52
                variazione_terapia_intensiva_3dma=record.variazione_terapia_intensiva_3dma,  # 53

                # 7DMA variation data
                variazione_casi_da_screening_7dma=record.variazione_casi_da_screening_7dma,  # 55
                variazione_casi_da_sospetto_diagnostico_7dma=record.variazione_casi_da_sospetto_diagnostico_7dma,  # 56
                variazione_casi_testati_7dma=record.variazione_casi_testati_7dma,  # 57
                variazione_deceduti_7dma=record.variazione_deceduti_7dma,  # 58
                variazione_dimessi_guariti_7dma=record.variazione_dimessi_guariti_7dma,  # 59
                variazione_isolamento_domiciliare_7dma=record.variazione_isolamento_domiciliare_7dma,  # 60
                variazione_ricoverati_con_sintomi_7dma=record.variazione_ricoverati_con_sintomi_7dma,  # 61
                variazione_tamponi_7dma=record.variazione_tamponi_7dma,  # 62
                variazione_terapia_intensiva_7dma=record.variazione_terapia_intensiva_7dma,  # 63

                # Others
                incidenza_7d=record.incidenza_7d,  # 64
                nuovi_positivi_7dma=record.nuovi_positivi_7dma,  # 65
                nuovi_positivi_3dma=record.nuovi_positivi_3dma,  # 66
                percentuale_positivi_tamponi=record.percentuale_positivi_tamponi,  # 67
                percentuale_positivi_tamponi_giornaliera=record.percentuale_positivi_tamponi_giornaliera,  # 68
                percentuale_positivi_casi=record.percentuale_positivi_casi,  # 69
                percentuale_positivi_casi_giornaliera=record.percentuale_positivi_casi_giornaliera,  # 70
                cfr=record.CFR, # 71

                nuovi_positivi_7dsum=record.nuovi_positivi_7dsum,
                nuovi_positivi_7d_incr=record.nuovi_positivi_7d_incr,
                terapia_intensiva_7dsum=record.terapia_intensiva_7dsum,
                terapia_intensiva_7d_incr=record.terapia_intensiva_7d_incr,
                deceduti_7dsum=record.deceduti_7dsum,
                deceduti_7d_incr=record.deceduti_7d_incr,
                dimessi_guariti_7dsum=record.dimessi_guariti_7dsum,
                dimessi_guariti_7d_incr=record.dimessi_guariti_7d_incr,
                ricoverati_con_sintomi_7dsum=record.ricoverati_con_sintomi_7dsum,
                ricoverati_con_sintomi_7d_incr=record.ricoverati_con_sintomi_7d_incr,
                ingressi_terapia_intensiva=record.ingressi_terapia_intensiva,
                percentuale_variazione_ingressi_terapia_intensiva=record.percentuale_variazione_ingressi_terapia_intensiva,
                variazione_ingressi_terapia_intensiva=record.variazione_ingressi_terapia_intensiva,
                variazione_ingressi_terapia_intensiva_3dma=record.variazione_ingressi_terapia_intensiva_3dma,
                variazione_ingressi_terapia_intensiva_7dma=record.variazione_ingressi_terapia_intensiva_7dma,
            )
            dato_regionale.save()
            count += 1
    logging.getLogger().info("Region data saved in DB")
    return count


def clean_region_from_db():
    RegioniItaliane.objects.all().delete()
    logging.getLogger().info("Region cleaned")


def clean_province_from_db():
    ProvinceItaliane.objects.all().delete()
    logging.getLogger().info("County cleaned")
