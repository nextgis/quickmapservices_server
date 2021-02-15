from django_filters import AllValuesFilter, CharFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.serializers import ModelSerializer, SlugRelatedField, ChoiceField
from rest_framework.viewsets import ModelViewSet

from ...models import GeoService, TmsService, WmsService, WfsService, ServiceIcon, GeoJsonService, GeoServiceStatus


# === Serializers
class GeoServiceGenericSerializer(ModelSerializer):
    cumulative_status = SlugRelatedField(many=False, source='last_status', slug_field='cumulative_status', read_only=True)


class GeoServiceSerializer(GeoServiceGenericSerializer):
    class Meta:
        model = GeoService
        fields = ('id', 'guid', 'name', 'desc', 'type', 'epsg', 'icon', 'submitter', 'created_at', 'updated_at', 'cumulative_status', 'extent')


class TmsServiceSerializer(GeoServiceGenericSerializer):
    class Meta:
        model = TmsService
        fields = '__all__'


class WmsServiceSerializer(GeoServiceGenericSerializer):
    class Meta:
        model = WmsService
        fields = '__all__'


class WfsServiceSerializer(GeoServiceGenericSerializer):
    class Meta:
        model = WfsService
        fields = '__all__'


class GeoJsonServiceSerializer(GeoServiceGenericSerializer):
    class Meta:
        model = GeoJsonService
        fields = '__all__'


class ServiceIconSerializer(ModelSerializer):
    class Meta:
        model = ServiceIcon
        fields = ('id', 'guid', 'name')


class GeoServiceStatusSerializer(ModelSerializer):
    class Meta:
        model = GeoServiceStatus
        fields = '__all__'

SERIALIZER_MAPPING = {
    TmsService.service_type: TmsServiceSerializer,
    WmsService.service_type: WmsServiceSerializer,
    WfsService.service_type: WfsServiceSerializer,
    GeoJsonService.service_type: GeoJsonServiceSerializer
}

# === Views Geoservices

class GeoServiceFilterSet(FilterSet):
    cumulative_status = AllValuesFilter(name="last_status__cumulative_status")
    intersects_extent = CharFilter(name='extent', lookup_expr='intersects')
    intersects_boundary = CharFilter(name='boundary', lookup_expr='intersects')

    class Meta:
        model = GeoService
        fields = ['type', 'epsg', 'submitter', 'cumulative_status']


class ServicePaginator(LimitOffsetPagination):
    default_limit = 100
    #max_limit = 500


class GeoServiceViewSet(ModelViewSet):
    base_name = 'geoservices'
    permission_classes = [IsAdminUser, ]
    pagination_class = ServicePaginator

    #TODO: def create() -> serializer + submitter

    def get_queryset(self):
        if self.action == 'list':
            return GeoService.objects.select_related('last_status')
        else:
            return GeoService.objects\
                .select_related('tmsservice')\
                .select_related('wmsservice')\
                .select_related('wfsservice')\
                .select_related('geojsonservice')\
                .select_related('last_status')

    def get_serializer_class(self, *args, **kwargs):
        if self.action == 'list':
            return GeoServiceSerializer

        if self.action == 'create':
            if 'type' in self.request.data.keys():
                return SERIALIZER_MAPPING.get(self.request.data['type'], GeoServiceSerializer)
            return GeoServiceSerializer

        instance = super(GeoServiceViewSet, self).get_object()
        if instance:
            return SERIALIZER_MAPPING.get(instance.type, GeoServiceSerializer)

        return GeoServiceSerializer

    def get_object(self):
        obj = super(GeoServiceViewSet, self).get_object()
        if obj:
            obj = obj.get_typed_instance()
        return obj

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filter_class = GeoServiceFilterSet

    search_fields = ('name', 'desc')
    ordering_fields = ('id', 'name', 'created_at', 'updated_at')
    ordering = ('name',)




