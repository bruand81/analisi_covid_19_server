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


def update_db():
    print('Check if update db is needed')
    latest_date_online = DatiRecenti().last_update_date
    print(f'Last online version of data is: {latest_date_online.strftime("%x")}')
    updated = False

    if RegioniItaliane.objects.exists():
        latest_date_in_db = RegioniItaliane.objects.latest('data').data
        print(f'Last last version in region DB: {latest_date_in_db.strftime("%x")}')
        if (latest_date_online - latest_date_in_db).days > 0:
            csv_to_db_regioni()
            updated = True
        else:
            if RegioniItaliane.objects.filter(data=latest_date_in_db).count() < 20:
                csv_to_db_regioni()
                updated = True
            else:
                print('Region update not needed')
    else:
        csv_to_db_regioni()
        updated = True

    if ProvinceItaliane.objects.exists():
        latest_date_in_db = ProvinceItaliane.objects.latest('data').data
        print(f'Last last version in county DB: {latest_date_in_db.strftime("%x")}')
        if (latest_date_online - latest_date_in_db).days > 0:
            csv_to_db_province()
            updated = True
        else:
            if ProvinceItaliane.objects.filter(data=latest_date_in_db).count() < 20:
                csv_to_db_regioni()
                updated = True
            else:
                print('Province update not needed')
    else:
        csv_to_db_province()
        updated = True

    if updated:
        logging.getLogger(__name__).info("Database updated")
        subject = 'Database app COVID 19 updated'
        message = ' Updated database for the app Covid 19'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['andrea.bruno@antaresnet.org', ]
        send_mail(subject, message, email_from, recipient_list)
    else:
        logging.getLogger(__name__).info("Database not updated")




def csv_to_db():
    csv_to_db_regioni()
    csv_to_db_province()


def csv_to_db_province():
    df = DatiProvince().dati_provinciali
    records = df.to_records()  # convert to records

    print("Saving county in DB")
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
            )
            dato_provinciale.save()
    print("County data saved in DB")


def csv_to_db_regioni():
    df = DatiRegioni().dati_completi
    records = df.to_records()  # convert to records

    print("Saving region in DB")
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
                percentuale_variazione_isolamento_domiciliare=record.percentuale_variazione_isolamento_domiciliare,  # 40
                percentuale_variazione_ricoverati_con_sintomi=record.percentuale_variazione_ricoverati_con_sintomi,  # 41
                percentuale_variazione_tamponi=record.percentuale_variazione_tamponi,  # 42
                percentuale_variazione_terapia_intensiva=record.percentuale_variazione_terapia_intensiva,  # 43

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
                cfr=record.CFR  # 71
            )
            dato_regionale.save()
    print("Region data saved in DB")
