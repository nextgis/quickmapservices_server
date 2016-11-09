from django.conf.urls import url, include

from qms_site.views import GeoserviceListView, GeoserviceDetailView, CreateServiceView

urlpatterns = [
    url(r'^$', GeoserviceListView.as_view(), name='site_geoservice_list'),
    url(r'^geoservices/(?P<pk>[0-9]+)/$', GeoserviceDetailView.as_view(), name='site_geoservice_detail'),
    url(r'', include('nextgis_common.ngid_auth.urls')),

    url(r'^create$', CreateServiceView.as_view(), name='create_service_view'),
]
