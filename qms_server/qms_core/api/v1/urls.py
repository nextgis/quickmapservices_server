from django.conf.urls import url

from .views import GeoServiceListView, GeoServiceDetailedView

urlpatterns = [
    url(r'^geoservice/$', GeoServiceListView.as_view()),
    url(r'^geoservice/(?P<pk>[0-9]+)/$', GeoServiceDetailedView.as_view()),
    #url(r'^geoservice/search/(?P<pk>+)/$', GeoServiceDetailedView.as_view()),

    # icons
    # popular
]
