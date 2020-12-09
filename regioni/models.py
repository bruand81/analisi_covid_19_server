from django.db import models


# Create your models here.
class RegioniItaliane(models.Model):
    # General Information
    index = models.IntegerField(primary_key=True)  # index
    data = models.DateTimeField()  # 72
    codice_regione = models.IntegerField()  # 18
    denominazione_regione = models.CharField(max_length=30)  # 19
    lat = models.FloatField()  # 20
    long = models.FloatField()  # 21

    # Direct source data
    ricoverati_con_sintomi = models.IntegerField()  # 3
    terapia_intensiva = models.IntegerField()  # 4
    totale_ospedalizzati = models.IntegerField()  # 5
    isolamento_domiciliare = models.IntegerField()  # 6
    totale_positivi = models.IntegerField()  # 7
    variazione_totale_positivi = models.IntegerField()  # 8
    nuovi_positivi = models.IntegerField()  # 9
    dimessi_guariti = models.IntegerField()  # 10
    deceduti = models.IntegerField()  # 11
    casi_da_sospetto_diagnostico = models.IntegerField()  # 12
    casi_da_screening = models.IntegerField()  # 13
    totale_casi = models.IntegerField()  # 14
    tamponi = models.IntegerField()  # 15
    casi_testati = models.IntegerField()  # 16
    popolazione = models.IntegerField()  # 22
    incidenza = models.FloatField()  # 23

    # Daily variation data
    variazione_casi_da_screening = models.IntegerField()  # 25
    variazione_casi_da_sospetto_diagnostico = models.IntegerField()  # 26
    variazione_casi_testati = models.IntegerField()  # 27
    variazione_deceduti = models.IntegerField()  # 28
    variazione_dimessi_guariti = models.IntegerField()  # 29
    variazione_isolamento_domiciliare = models.IntegerField()  # 30
    variazione_ricoverati_con_sintomi = models.IntegerField()  # 31
    variazione_tamponi = models.IntegerField()  # 32
    variazione_terapia_intensiva = models.IntegerField()  # 33
    percentuale_variazione_casi_da_screening = models.FloatField()  # 35
    percentuale_variazione_casi_da_sospetto_diagnostico = models.FloatField()  # 36
    percentuale_variazione_casi_testati = models.FloatField()  # 37
    percentuale_variazione_deceduti = models.FloatField()  # 38
    percentuale_variazione_dimessi_guariti = models.FloatField()  # 39
    percentuale_variazione_isolamento_domiciliare = models.FloatField()  # 40
    percentuale_variazione_ricoverati_con_sintomi = models.FloatField()  # 41
    percentuale_variazione_tamponi = models.FloatField()  # 42
    percentuale_variazione_terapia_intensiva = models.FloatField()  # 43
    percentuale_positivi_casi_7dma = models.FloatField()
    percentuale_positivi_casi_3dma = models.FloatField()

    # 3DMA variation data
    variazione_casi_da_screening_3dma = models.IntegerField()  # 45
    variazione_casi_da_sospetto_diagnostico_3dma = models.IntegerField()  # 46
    variazione_casi_testati_3dma = models.IntegerField()  # 47
    variazione_deceduti_3dma = models.IntegerField()  # 48
    variazione_dimessi_guariti_3dma = models.IntegerField()  # 49
    variazione_isolamento_domiciliare_3dma = models.IntegerField()  # 50
    variazione_ricoverati_con_sintomi_3dma = models.IntegerField()  # 51
    variazione_tamponi_3dma = models.IntegerField()  # 52
    variazione_terapia_intensiva_3dma = models.IntegerField()  # 53

    # 7DMA variation data
    variazione_casi_da_screening_7dma = models.IntegerField()  # 55
    variazione_casi_da_sospetto_diagnostico_7dma = models.IntegerField()  # 56
    variazione_casi_testati_7dma = models.IntegerField()  # 57
    variazione_deceduti_7dma = models.IntegerField()  # 58
    variazione_dimessi_guariti_7dma = models.IntegerField()  # 59
    variazione_isolamento_domiciliare_7dma = models.IntegerField()  # 60
    variazione_ricoverati_con_sintomi_7dma = models.IntegerField()  # 61
    variazione_tamponi_7dma = models.IntegerField()  # 62
    variazione_terapia_intensiva_7dma = models.IntegerField()  # 63

    # Others
    incidenza_7d = models.FloatField()  # 64
    nuovi_positivi_7dma = models.IntegerField()  # 65
    nuovi_positivi_3dma = models.IntegerField()  # 66
    percentuale_positivi_tamponi = models.FloatField()  # 67
    percentuale_positivi_tamponi_giornaliera = models.FloatField()  # 68
    percentuale_positivi_casi = models.FloatField()  # 69
    percentuale_positivi_casi_giornaliera = models.FloatField()  # 70
    cfr = models.FloatField()  # 71

    nuovi_positivi_7d_incr = models.IntegerField(default=0)
    nuovi_positivi_7dsum = models.IntegerField(default=0)
    terapia_intensiva_7dsum = models.IntegerField(default=0)
    terapia_intensiva_7d_incr = models.IntegerField(default=0)
    deceduti_7dsum = models.IntegerField(default=0)
    deceduti_7d_incr = models.IntegerField(default=0)
    dimessi_guariti_7dsum = models.IntegerField(default=0)
    dimessi_guariti_7d_incr = models.IntegerField(default=0)
    ricoverati_con_sintomi_7dsum = models.IntegerField(default=0)
    ricoverati_con_sintomi_7d_incr = models.IntegerField(default=0)
    ingressi_terapia_intensiva = models.IntegerField(default=0)
    percentuale_variazione_ingressi_terapia_intensiva = models.FloatField(default=0)
    variazione_ingressi_terapia_intensiva = models.IntegerField(default=0)
    variazione_ingressi_terapia_intensiva_3dma = models.IntegerField(default=0)
    variazione_ingressi_terapia_intensiva_7dma = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Riepilogo Italia'
        verbose_name_plural = 'Riepilogo Italia'
