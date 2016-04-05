from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter, DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from qms_core.models import GeoService, TmsService, WmsService, WfsService

# === Serializers

class GeoServiceSerializer(ModelSerializer):
    class Meta:
        model = GeoService
        fields = ('id', 'guid', 'name', 'desc', 'type')


class TmsServiceSerializer(ModelSerializer):
    class Meta:
        model = TmsService
        fields = '__all__'


class WmsServiceSerializer(ModelSerializer):
    class Meta:
        model = WmsService
        fields = '__all__'


class WfsServiceSerializer(ModelSerializer):
    class Meta:
        model = WfsService
        fields = '__all__'



# === Views

class GeoServiceListView(ListAPIView):
    queryset = GeoService.objects.all()
    serializer_class = GeoServiceSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    filter_fields = ('type',)
    search_fields = ('name', 'desc')


class GeoServiceDetailedView(RetrieveAPIView):
    queryset = GeoService.objects.select_related('tmsservice').select_related('wmsservice').select_related('wfsservice')

    def get_object(self):
        obj = super(GeoServiceDetailedView, self).get_object()
        if obj:
            if obj.type == TmsService.service_type:
                obj = obj.tmsservice
            if obj.type == WmsService.service_type:
                obj = obj.wmsservice
            if obj.type == WfsService.service_type:
                obj = obj.wfsservice
        return obj

    def get_serializer(self, instance):
        if instance:
            if instance.type == TmsService.service_type:
                return TmsServiceSerializer(instance)
            if instance.type == WmsService.service_type:
                return WmsServiceSerializer(instance)
            if instance.type == WfsService.service_type:
                return WfsServiceSerializer(instance)
        return GeoServiceSerializer(instance)



# === API ROOT and others


class ApiRootView(APIView):

    def get(self, request, format=None):
        return Response({
            'geoservices_url': reverse('geoservice_list', request=request, format=format),
            #'geoservices_search_url': reverse('geoservice_list', request=request, format=format) + '?search={query}',
            #'snippets': reverse('snippet-list', request=request, format=format)
        })

