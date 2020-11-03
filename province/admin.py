from django.contrib import admin

# Register your models here.
from province.models import ProvinceItaliane


@admin.register(ProvinceItaliane)
class ProvinceItalianeAdmin(admin.ModelAdmin):
    list_display = ("data", "denominazione_regione", "denominazione_provincia", "totale_casi", "variazione_totale_casi", "incidenza", "incidenza_7d", "variazione_totale_casi_7dma")
    list_filter = ("data", "denominazione_regione", "denominazione_provincia")