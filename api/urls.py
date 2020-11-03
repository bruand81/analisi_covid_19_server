from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'regioni', views.RegioniItalianeViewSet)
router.register(r'province', views.ProvinceItalianeViewSet)
router.register(r'riepilogo', views.RiepilogoRegioniViewSet)
router.register(r'list', views.RegioniListViewsSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
