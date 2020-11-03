from datetime import datetime, timedelta

import pytz
from django.shortcuts import render
from django.views import generic


# Create your views here.
from province.models import ProvinceItaliane


class IndexView(generic.ListView):
    template_name = 'province/index.html'
    context_object_name = 'all_county_data'

    def get_queryset(self):
        d = pytz.utc.localize(datetime.now() - timedelta(days=1))
        return ProvinceItaliane.objects.filter(data__gte=d).order_by('-data')
