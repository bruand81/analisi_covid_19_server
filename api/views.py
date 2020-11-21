from datetime import datetime, timedelta

import pytz
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny

from province.models import ProvinceItaliane
from .serializers import RegioniItalianeSerializer, ProvinceItalianeSerializer#, RiepilogoRegioniSerializer, \
    # RegioniListSerializer
from regioni.models import RegioniItaliane


def parse_max_days(max_days) -> int:
    try:
        d = int(max_days)
        return d
    except ValueError:
        return 0
    except TypeError:
        return 0


class StandardResultsSetPagination(LimitOffsetPagination):
    default_limit = 100
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 1000


# class RegioniListViewsSet(viewsets.ReadOnlyModelViewSet):
#     queryset = RegioniItaliane.objects.filter(codice_regione__gte=1).values('codice_regione', 'denominazione_regione').order_by('denominazione_regione').distinct()
#     serializer_class = RegioniListSerializer
#     permission_classes = [AllowAny]
#     pagination_class = None
#
#
# class RiepilogoRegioniViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = RegioniItaliane.objects.all()
#     serializer_class = RiepilogoRegioniSerializer
#     filter_backends = [
#         DjangoFilterBackend,
#         SearchFilter,
#         OrderingFilter
#     ]
#     filterset_fields = ['codice_regione', 'data']
#     search_fields = ['denominazione_regione']
#     ordering_fields = ['data', 'codice_regione']
#     ordering = ['data']
#     permission_classes = [AllowAny]
#     pagination_class = None
#
#     def get_queryset(self):
#         max_date = RegioniItaliane.objects.latest('data').data
#         startdate = max_date - timedelta(days=30)
#         return RegioniItaliane.objects.filter(data__gte=startdate)


class RegioniItalianeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RegioniItaliane.objects.all().order_by('-data')
    serializer_class = RegioniItalianeSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ['codice_regione', 'data', 'index']
    search_fields = ['denominazione_regione']
    ordering_fields = ['data', 'codice_regione']
    ordering = ['-data']
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = RegioniItaliane.objects.all()
        max_days = parse_max_days(self.request.query_params.get('max_days', None))
        if max_days >= 0:
            try:
                max_days = max_days if max_days > 0 else 1
                hours = 23+((max_days-1)*24)
                d = RegioniItaliane.objects.latest('data').data - timedelta(hours=hours)
                return RegioniItaliane.objects.filter(data__gte=d)
            except RegioniItaliane.DoesNotExist:
                raise Http404
        return queryset


class ProvinceItalianeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProvinceItaliane.objects.all().order_by('-data')
    serializer_class = ProvinceItalianeSerializer
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    ]
    filterset_fields = ['codice_regione', 'codice_provincia', 'data', 'index']
    search_fields = ['denominazione_regione', 'denominazione_provincia']
    ordering_fields = ['data', 'codice_regione', 'codice_provincia']
    ordering = ['-data']
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = ProvinceItaliane.objects.all()
        max_days = parse_max_days(self.request.query_params.get('max_days', None))
        if max_days >= 0:
            try:
                max_days = max_days if max_days > 0 else 1
                hours = 23 + ((max_days - 1) * 24)
                d = ProvinceItaliane.objects.latest('data').data - timedelta(hours=hours)
                return ProvinceItaliane.objects.filter(data__gte=d)
            except RegioniItaliane.DoesNotExist:
                raise Http404
        return queryset
