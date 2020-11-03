from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'regioni', views.RegioniItalianeViewSet, 'regioni')
router.register(r'province', views.ProvinceItalianeViewSet, 'province')
router.register(r'riepilogoregioni', views.RiepilogoRegioniViewSet, 'riepilogoregioni')
router.register(r'listregioni', views.RegioniListViewsSet, 'listregioni')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
