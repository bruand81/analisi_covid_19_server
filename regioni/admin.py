from django.contrib import admin

# Register your models here.
from regioni.models import RegioniItaliane


@admin.register(RegioniItaliane)
class RegioniItalianeAdmin(admin.ModelAdmin):
    list_display = ("denominazione_regione", "data", "nuovi_positivi", "variazione_deceduti", "variazione_terapia_intensiva",
                    "variazione_ricoverati_con_sintomi", "percentuale_positivi_casi_giornaliera", "incidenza_7d")
    list_filter = ("denominazione_regione", "data")
