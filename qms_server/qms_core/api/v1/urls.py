from django.conf.urls import url

from .views import GeoServiceListView, GeoServiceDetailedView, ApiRootView, ServiceIconListView, ServiceIconDetailedView, \
    IconRetrieveView, DefaultIconRetrieveView

urlpatterns = [
    url(r'^$', ApiRootView.as_view(), name='api_root'),

    url(r'^geoservices/$', GeoServiceListView.as_view(), name='geoservice_list'),
    url(r'^geoservices/(?P<pk>[0-9]+)/$', GeoServiceDetailedView.as_view(), name='geoservice_detail'),

    # icons
    url(r'^icons/$', ServiceIconListView.as_view(), name='service_icon_list'),
    url(r'^icons/(?P<pk>[0-9]+)/$', ServiceIconDetailedView.as_view(), name='service_icon_detail'),
    url(r'^icons/(?P<pk>[0-9]+)/content$', IconRetrieveView.as_view(), name='service_icon_retrieve'),
    url(r'^icons/default$', DefaultIconRetrieveView.as_view(), name='service_icon_default'),
    url(r'^icons/default/content$', DefaultIconRetrieveView.as_view(), name='service_icon_default_alias'),

    # popular
]
