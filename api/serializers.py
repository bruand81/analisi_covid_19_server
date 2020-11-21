from rest_framework import serializers

from regioni.models import RegioniItaliane
from province.models import ProvinceItaliane


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        fields = self.context['request'].query_params.get('fields')
        if fields:
            fields = fields.split(',')
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class ProvinceItalianeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProvinceItaliane
        fields = '__all__'


class RegioniItalianeSerializer(DynamicFieldsModelSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RegioniItaliane
        fields = '__all__'


# class RegioniListSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = RegioniItaliane
#         fields = [
#             'codice_regione',
#             'denominazione_regione'
#         ]
#
#
# class RiepilogoRegioniSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = RegioniItaliane
#         fields = [
#             'data',
#             'codice_regione',
#             'denominazione_regione',
#             'nuovi_positivi',
#             'variazione_deceduti',
#             'variazione_dimessi_guariti',
#             'variazione_ricoverati_con_sintomi',
#             'variazione_terapia_intensiva',
#             'variazione_tamponi',
#             'incidenza_7d',
#             'nuovi_positivi_7dma',
#             'nuovi_positivi_3dma',
#             'incidenza',
#             'percentuale_positivi_casi_giornaliera',
#             'percentuale_variazione_terapia_intensiva',
#             'percentuale_variazione_deceduti',
#             'percentuale_positivi_casi_7dma',
#             'cfr',
#             'variazione_terapia_intensiva_7dma',
#             'variazione_deceduti_7dma',
#             'variazione_ricoverati_con_sintomi_7dma'
#         ]
