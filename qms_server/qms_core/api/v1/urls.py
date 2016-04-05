from django.conf.urls import url

from .views import GeoServiceListView, GeoServiceDetailedView, ApiRootView

urlpatterns = [
    url(r'^$', ApiRootView.as_view(), name='api_root'),

    url(r'^geoservices/$', GeoServiceListView.as_view(), name='geoservice_list'),
    url(r'^geoservices/(?P<pk>[0-9]+)/$', GeoServiceDetailedView.as_view(), name='geoservice_detail'),

    # icons
    # popular
]
