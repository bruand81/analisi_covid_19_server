from rest_framework import serializers

from regioni.models import RegioniItaliane
from province.models import ProvinceItaliane


class ProvinceItalianeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProvinceItaliane
        fields = '__all__'


class RegioniItalianeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RegioniItaliane
        fields = '__all__'


class RegioniListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RegioniItaliane
        fields = [
            'codice_regione',
            'denominazione_regione'
        ]


class RiepilogoRegioniSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RegioniItaliane
        fields = [
            'data',
            'codice_regione',
            'denominazione_regione',
            'nuovi_positivi',
            'variazione_deceduti',
            'variazione_dimessi_guariti',
            'variazione_ricoverati_con_sintomi',
            'variazione_terapia_intensiva',
            'variazione_tamponi',
            'incidenza_7d',
            'nuovi_positivi_7dma',
            'nuovi_positivi_3dma',
            'incidenza',
            'percentuale_positivi_casi_giornaliera',
            'percentuale_variazione_terapia_intensiva',
            'percentuale_variazione_deceduti',
            'cfr'
        ]
