import os
import random
import datetime

from django_filters import AllValuesFilter, CharFilter
from django.db.models import Q
#from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter, OrderingFilter 
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, OrderedDict, SlugRelatedField, SerializerMethodField
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import status
from rest_framework import authentication
from rest_framework import permissions

from qms_site.models import UserReport

from ...icon_renderer import IconRenderer
from ...icon_serializer import IconSerializer
from ...models import GeoService, TmsService, WmsService, WfsService, ServiceIcon, GeoJsonService, GeoServiceStatus, CumulativeStatus

# from qms_core.status_checker.status_checker import check_by_id_and_save
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from django.conf import settings

# === Serializers
class GeoServiceGenericSerializer(ModelSerializer):
    cumulative_status = SlugRelatedField(many=False, source='last_status', slug_field='cumulative_status', read_only=True)


class GeoServiceSerializer(GeoServiceGenericSerializer):
    class Meta:
        model = GeoService
        fields = ('id', 'guid', 'name', 'desc', 'type', 'epsg', 'icon', 'submitter', 'created_at', 'updated_at', 'cumulative_status', 'extent')


class GeoServiceCreationSerializer(GeoServiceGenericSerializer):
    class Meta:
        model = GeoService
        fields = (
            'name', 
            'desc', 
            'type', 
            'epsg', 
            'icon', 
            'license_name',
            'license_url',
            'copyright_text',
            'copyright_url',
            'terms_of_use_url',
            'extent',
            'boundary',
            'boundary_area',
            'source',
            'source_url'
        )

    # def create(self, validated_data):
        # obj = super(GeoServiceCreationSerializer, self).create(validated_data)
        # checking may take a long time
        # check_by_id_and_save(obj.id)
        # return obj


class TmsServiceModificationSerializer(GeoServiceCreationSerializer):
    class Meta:
        model = TmsService
        fields = GeoServiceCreationSerializer.Meta.fields + (
            'url',
            'z_min',
            'z_max',
            'y_origin_top',
        )
    
   
class WmsServiceModificationSerializer(GeoServiceCreationSerializer):
    class Meta:
        model = WmsService
        fields = GeoServiceCreationSerializer.Meta.fields + (
            'url',
            'params',
            'layers',
            'turn_over',
            'format'
        )


class WfsServiceModificationSerializer(GeoServiceCreationSerializer):
    class Meta:
        model = WfsService
        fields = GeoServiceCreationSerializer.Meta.fields + (
            'url',
            'layer'
        )
        extra_kwargs_on_update = {
            'url': {'required': False}, 
            'layer': {'required': False},
            'type': {'required': False},
            'name': {'required': False}
        }


class GeoJsonServiceModificationSerializer(GeoServiceCreationSerializer):
    class Meta:
        model = GeoJsonService
        fields = GeoServiceCreationSerializer.Meta.fields + (
            'url',
        )


class TmsServiceSerializer(GeoServiceGenericSerializer):
    url = SerializerMethodField()
    alt_urls = SerializerMethodField()
    origin_url = SerializerMethodField()

    class Meta:
        model = TmsService
        fields = '__all__'

    def get_origin_url(self, obj):
        return obj.url

    def get_alt_urls(self, obj):
        return self.__generate_alt_urls(obj)

    def get_url(self, obj):
        alt_urls = self.__generate_alt_urls(obj)
        if len(alt_urls) == 0:
            tms_url = obj.url
        else:
            tms_url = alt_urls[random.randint(0, len(alt_urls)-1)]

        return tms_url

    def __generate_alt_urls(self, obj):
        url_pattern, subdomains = obj.get_url_pattern_and_subdomains()
        urls = []
        for subdomain in subdomains:
            urls.append(
                url_pattern % {'subdomain': subdomain}
            )
        return urls

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



# === Views Geoservices

class GeoServiceFilterSet(FilterSet):
    cumulative_status = AllValuesFilter(field_name="last_status__cumulative_status")
    intersects_extent = CharFilter(field_name='extent', lookup_expr='intersects')
    intersects_boundary = CharFilter(field_name='boundary', lookup_expr='intersects')

    class Meta:
        model = GeoService
        fields = ['type', 'epsg', 'submitter', 'cumulative_status']


class GeoServiceListView(ListAPIView):
    queryset = GeoService.objects.select_related('last_status')
    serializer_class = GeoServiceSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filter_class = GeoServiceFilterSet
    search_fields = ('name', 'desc')
    ordering_fields = ('id', 'name', 'created_at', 'updated_at')
    ordering = ('name',)

class AuthorizedCompanyUser(permissions.BasePermission):
    def has_permission(self, request, view):

        meta = request.META
        http_auth = meta.get('HTTP_AUTHORIZATION')
        if http_auth:
            if http_auth == settings.MODIFICATION_API_BASIC_AUTH:
                return True

        user = request.user
        if user.groups.filter(name='MODIFICATION_API_USERS').exists():
            return True

        if request.method == 'DELETE':
            #
            #   TODO: refactor
            #
            pc = request.parser_context['kwargs']
            if not pc:
                return False
            guid = pc.get('guid')
            if not guid:
                return False
            geo_service = GeoService.objects.filter(guid=guid).get()
            if not geo_service:
                return False
            if geo_service.submitter == user:
                return True

        return False


class CsrfExemptSessionAuthentication(authentication.SessionAuthentication):
    def enforce_csrf(self, request):
        return


class GeoServiceModificationMixin:
    queryset = GeoService.objects.all()
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (AuthorizedCompanyUser,)
    serializer_class = GeoServiceCreationSerializer

    def get_object(self):
        kw = self.kwargs
        guid_val = kw.get('guid')
        obj_type = GeoService.objects.filter(guid=guid_val).values_list('type', flat=True).get()
        cls = GeoService.get_typed_class(obj_type)
        obj = cls.objects.filter(guid=guid_val).first()
        return obj

    def get_serializer_class(self):
        service_type = None
        if hasattr(self, 'service_type'):
            service_type = self.service_type
        serializer_class = self._get_modification_serializer_class( service_type )
        return serializer_class

    def _get_modification_serializer_class(self, service_type):
        if service_type == TmsService.service_type:
            return TmsServiceModificationSerializer
        if service_type == WmsService.service_type:
            return WmsServiceModificationSerializer
        if service_type == WfsService.service_type:
            return WfsServiceModificationSerializer
        if service_type == GeoJsonService.service_type:
            return GeoJsonServiceModificationSerializer
        return GeoServiceModificationMixin

    def check_fields(self, serializer, request):
        serializer_fields = serializer.Meta.fields
        for field in request.data:
            if field not in serializer_fields:
                raise Exception(field + ' field is not allowed. Allowed fields: ' + str(serializer_fields))

    def _make_result(self, str_status, str_message, guid):
        result = {'status': str_status}
        if guid:
            result['guid'] = guid
        if str_message:
            result['message'] = str_message

        return result

    def _handle_exception(self, str_status, str_message, e):
        str_status = 'failed'
        str_message = str(e)

        return str_status, str_message

    
class GeoServiceCreateView(GeoServiceModificationMixin, CreateAPIView):
    # https://stackoverflow.com/a/54993327
    # https://stackoverflow.com/a/36786134
    def create(self, request, *args, **kwargs):
        str_status = 'ok'
        str_message = ''
        guid = ''
        
        self.service_type = request.data.get('type')

        user = request.user
        submitter = None
        try:
            types = GeoService.get_valid_service_types()
            if self.service_type not in types:
                raise Exception('wrong service type ')

            if isinstance(user, AnonymousUser):
                user_model = get_user_model()
                user = user_model.objects.filter(username=settings.CREATION_THROUGH_API_SUBMITTER)
                if user:
                    user = user.get()
                    submitter = user
            serializer = self.get_serializer(data=request.data)

            self.check_fields(serializer, request)
            
            serializer.is_valid(raise_exception=True)
            instance = serializer.save(submitter=submitter)
            instance.updated_at = datetime.datetime.now()
            instance.save() 
            
            guid = instance.guid
        except Exception as e:
            str_status, str_message = self._handle_exception(str_status, str_message, e)

        result = self._make_result(str_status, str_message, guid)
        
        return Response(result, status=status.HTTP_201_CREATED)


class GeoServiceUpdateView(GeoServiceModificationMixin, RetrieveUpdateAPIView):
    lookup_field = 'guid'

    def update(self, request, *args, **kwargs):
        str_status = 'ok'
        str_message = ''
        guid = ''

        try:
            instance = self.get_object()
            self.service_type = instance.type
            request_service_type = request.data.get('type')

            if request_service_type:
                raise Exception('do not specify service type in update operation')
            if not request.data:
                raise Exception('empty data not allowed in update operation')
            serializer = self.get_serializer(data=request.data, partial=True)

            self.check_fields(serializer, request)

            serializer.is_valid(raise_exception=True)
            instance.updated_at = datetime.datetime.now()
            instance = serializer.update(instance, serializer.validated_data) 
            
            guid = instance.guid
        except Exception as e:
            str_status, str_message = self._handle_exception(str_status, str_message, e)

        result = self._make_result(str_status, str_message, guid)
        
        return Response(result, status=status.HTTP_200_OK)


class GeoServiceDeleteView(GeoServiceModificationMixin, DestroyAPIView):
    lookup_field = 'guid'

    def delete(self, request, *args, **kwargs):
        str_status = 'ok'
        str_message = ''
        guid = ''

        try:
            instance = self.get_object()
            guid = instance.guid
            service_id = instance.id
            reports = UserReport.objects.filter(geo_service_id=service_id)
            reports.delete()
            self.perform_destroy(instance)

        except Exception as e:
            str_status, str_message = self._handle_exception(str_status, str_message, e)

        result = self._make_result(str_status, str_message, guid)
        
        return Response(result, status=status.HTTP_200_OK)


class GeoServiceDetailedView(RetrieveAPIView):
    queryset = GeoService.objects\
        .select_related('tmsservice')\
        .select_related('wmsservice')\
        .select_related('wfsservice')\
        .select_related('geojsonservice')\
        .select_related('last_status')

    def get_object(self):
        obj = super(GeoServiceDetailedView, self).get_object()
        if obj:
            if obj.type == TmsService.service_type:
                obj = obj.tmsservice
            if obj.type == WmsService.service_type:
                obj = obj.wmsservice
            if obj.type == WfsService.service_type:
                obj = obj.wfsservice
            if obj.type == GeoJsonService.service_type:
                obj = obj.geojsonservice
        return obj

    def get_serializer(self, instance):
        if instance:
            if instance.type == TmsService.service_type:
                return TmsServiceSerializer(instance)
            if instance.type == WmsService.service_type:
                return WmsServiceSerializer(instance)
            if instance.type == WfsService.service_type:
                return WfsServiceSerializer(instance)
            if instance.type == GeoJsonService.service_type:
                return GeoJsonServiceSerializer(instance)

        return GeoServiceSerializer(instance)

# === Views statuses
class ServiceStatusPaginator(LimitOffsetPagination):
    default_limit = 100
    max_limit = 500


class GeoServiceStatusViewSet(ReadOnlyModelViewSet):
    pagination_class = ServiceStatusPaginator
    queryset = GeoServiceStatus.objects.all()
    serializer_class = GeoServiceStatusSerializer
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    filter_fields = ('geoservice', 'cumulative_status',)
    ordering_fields = ('check_at', 'cumulative_status')
    ordering = ('check_at',)


# === Views Icons

class ServiceIconListView(ListAPIView):
    queryset = ServiceIcon.objects.all()
    serializer_class = ServiceIconSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ('name',)


class ServiceIconDetailedView(RetrieveAPIView):
    queryset = ServiceIcon.objects.all()
    serializer_class = ServiceIconSerializer


class IconRetrieveView(RetrieveAPIView):
    queryset = ServiceIcon.objects.all()
    serializer_class = IconSerializer
    renderer_classes = [IconRenderer, ]


class DefaultIconRetrieveView(APIView):
    renderer_classes = [IconRenderer, ]

    def get(self, request, *args, **kwargs):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return Response(open(os.path.join(BASE_DIR, os.pardir, 'static/qms_core/img/default_icon.png'), mode='rb'))


# === API ROOT and others

class ApiRootView(APIView):

    def get(self, request, format=None):
        temp_rep_val = 2110112
        simple_url = lambda name: reverse(name, request=request, format=format)
        repl_id_ulr = lambda name: reverse(name,
                                           kwargs={'pk': temp_rep_val},
                                           request=request,
                                           format=format).replace(str(temp_rep_val), '{id}')

        return Response(OrderedDict((
            ('geoservices_url', simple_url('geoservice_list')),
            ('geoservices_type_filter_url', simple_url('geoservice_list') + '?type={tms|wms|wfs|geojson}'),
            ('geoservices_epsg_filter_url', simple_url('geoservice_list') + '?epsg={any_epsg_code}'),
            ('geoservices_status_filter_url', simple_url('geoservice_list') + '?cumulative_status={works|problematic|failed}'),
            ('geoservices_search_url', simple_url('geoservice_list') + '?search={q}'),
            ('geoservices_intersects_extent_url', simple_url('geoservice_list') + '?intersects_extent={WKT|EWKT geometry}'),
            ('geoservices_intersects_boundary_url', simple_url('geoservice_list') + '?intersects_boundary={WKT|EWKT geometry}'),
            ('geoservices_ordering_url', simple_url('geoservice_list') + '?ordering={name|-name|id|-id|created_at|-created_at|updated_at|-updated_at'),
            ('geoservices_pagination_url', simple_url('geoservice_list') + '?limit={int}&offset={int}'),

            ('geoservice_detail_url', repl_id_ulr('geoservice_detail')),

            ('geoservice_status_url', simple_url('geoservicestatus-list')),
            ('geoservice_status_detail_url', repl_id_ulr('geoservicestatus-detail')),
            ('geoservice_status_service_filter_url', simple_url('geoservicestatus-list') + '?geoservice={id}'),
            ('geoservice_status_cumulative_status_filter_url', simple_url('geoservicestatus-list') + '?cumulative_status={works|problematic|failed}'),
            ('geoservice_status_check_at_ordering_url', simple_url('geoservicestatus-list') + '?ordering={check_at|-check_at}'),

            ('icons_url', simple_url('service_icon_list')),
            ('icons_search_url', simple_url('service_icon_list') + '?search={q}'),
            ('icons_pagination_url', simple_url('service_icon_list') + '?limit={int}&offset={int}'),
            ('icon_detail_url', repl_id_ulr('service_icon_detail')),
            ('icon_content_url', repl_id_ulr('service_icon_retrieve')),
            ('icon_resized_content_url', repl_id_ulr('service_icon_retrieve') + '?width={16<=x<=64}&height={16<=y<=64}'),
            ('default_icon_url', simple_url('service_icon_default'))
        )))
