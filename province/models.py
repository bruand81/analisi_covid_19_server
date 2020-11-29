from django.db import models


# Create your models here.
class ProvinceItaliane(models.Model):
    # General Information
    index = models.IntegerField(primary_key=True)
    data = models.DateTimeField()
    codice_regione = models.IntegerField()
    denominazione_regione = models.CharField(max_length=30)
    codice_provincia = models.IntegerField()
    denominazione_provincia = models.CharField(max_length=30)
    sigla_provincia = models.CharField(max_length=10)
    lat = models.FloatField()
    long = models.FloatField()

    # Data Field
    totale_casi = models.IntegerField()
    incidenza = models.FloatField()
    variazione_totale_casi = models.IntegerField()
    percentuale_variazione_totale_casi = models.FloatField()
    variazione_totale_casi_3dma = models.IntegerField()
    variazione_totale_casi_7dma = models.IntegerField()
    incidenza_7d = models.FloatField()
    nuovi_positivi_7dsum = models.IntegerField(default=0)
    nuovi_positivi_7d_incr = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Riepilogo Province'
        verbose_name_plural = 'Riepilogo Province'
