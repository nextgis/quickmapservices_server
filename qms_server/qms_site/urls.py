from django.conf.urls import url, include

from qms_site.views import GeoserviceListView, GeoserviceDetailView, GeoserviceBoundaryView, CreateServiceView, EditServiceView, AboutView, FAQView

urlpatterns = [
    url(r'^$', GeoserviceListView.as_view(), name='site_geoservice_list'),
    url(r'^about$', AboutView.as_view(), name='site_about'),
    url(r'^faq$', FAQView.as_view(), name='site_faq'),
    url(r'^geoservices/(?P<pk>[0-9]+)/$', GeoserviceDetailView.as_view(), name='site_geoservice_detail'),
    url(r'^geoservices/(?P<pk>[0-9]+)/boundary$', GeoserviceBoundaryView.as_view(), name='site_geoservice_boundary'),
    url(r'', include('nextgis_common.ngid_auth.urls')),

    url(r'^create$', CreateServiceView.as_view(), name='create_service_view'),
    url(r'^edit/(?P<pk>[0-9]+)/$', EditServiceView.as_view(), name='edit_service_view'),
]
