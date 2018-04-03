from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib.gis.db.models import PolygonField, MultiPolygonField
from django import forms
from django.core import urlresolvers
from django.templatetags.static import static
from django.utils.translation import ugettext as _
from qms_core.models import NextgisUser, GeoService, TmsService, WmsService, WfsService, ServiceIcon, GeoJsonService, \
    GeoServiceStatus


@admin.register(NextgisUser)
class NextgisUserAdmin(UserAdmin):

    readonly_fields = ('nextgis_id', 'nextgis_guid')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('NextGIS ID'), {'fields': ('nextgis_id', 'nextgis_guid',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


# GENERIC SERVICE
common_fieldset = (_('Common'), {'fields': ('guid', 'type', 'name', 'desc', 'epsg', 'icon', 'cumulative_status')})
license_fieldset = (_('License & Copyright'), {'fields': ('license_name', 'license_url', 'copyright_text', 'copyright_url', 'terms_of_use_url')})
source_fieldset = (_('Source info'), {'fields': ('source', 'source_url')})
boundary_fields = (_('Boundary'), {'fields': ('extent', 'boundary', 'boundary_area')})


class GenericServiceAdmin(admin.ModelAdmin):  #OSMGeoAdmin
    formfield_overrides = {
        PolygonField: {'widget': forms.Textarea},
        MultiPolygonField: {'widget': forms.Textarea},
    }

    openlayers_url = static('qms_core/js/OpenLayers.js')

    readonly_fields = ('guid', 'type', 'cumulative_status')
    list_display = ('id', 'name', 'cumulative_status', 'desc')
    search_fields = ('name', 'desc')

    def cumulative_status(self, obj):
        if obj.last_status:
            base_url = urlresolvers.reverse('admin:qms_core_geoservicestatus_change', args=(obj.last_status.id,))
            return '<a href="%s" target=_blank>%s</a>' % (base_url, str(obj.last_status.cumulative_status))
        else:
            return None
    cumulative_status.allow_tags = True
    cumulative_status.admin_order_field = 'last_status__cumulative_status'
    cumulative_status.admin_filter_field = 'last_status__cumulative_status'
    cumulative_status.short_description = 'Cumulative status'



@admin.register(GeoService)
class GeoServiceAdmin(GenericServiceAdmin):
    readonly_fields = (
        'id', 'guid', 'name', 'desc', 'type', 'epsg', 'icon',
        'license_name', 'license_url', 'copyright_text', 'copyright_url', 'terms_of_use_url',
        'submitter', 'created_at', 'updated_at', 'source', 'source_url',
        'cumulative_status', 'last_status'
    )

    list_display = ('id', 'type', 'name', 'desc', 'cumulative_status', )
    list_filter = ('type', )
    search_fields = ('name', 'desc')


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



@admin.register(TmsService)
class TmsServiceAdmin(GenericServiceAdmin):

    fieldsets = (
        common_fieldset,
        license_fieldset,
        source_fieldset,
        boundary_fields,
        (_('TMS'), {'fields': ('url', 'z_min', 'z_max', 'y_origin_top')}),
    )


@admin.register(WmsService)
class WmsServiceAdmin(GenericServiceAdmin):

    fieldsets = (
        common_fieldset,
        license_fieldset,
        source_fieldset,
        boundary_fields,
        (_('WMS'), {'fields': ('url', 'params', 'layers', 'turn_over', 'format')}),
    )


@admin.register(WfsService)
class WfsServiceAdmin(GenericServiceAdmin):

    fieldsets = (
        common_fieldset,
        license_fieldset,
        source_fieldset,
        boundary_fields,
        (_('WFS'), {'fields': ('url', 'layer')}),
    )


@admin.register(GeoJsonService)
class GeoJsonServiceAdmin(GenericServiceAdmin):

    fieldsets = (
        common_fieldset,
        license_fieldset,
        source_fieldset,
        boundary_fields,
        (_('GeoJSON'), {'fields': ('url', )}),
    )


@admin.register(ServiceIcon)
class ServiceIconAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )


@admin.register(GeoServiceStatus)
class GeoServiceStatusAdmin(admin.ModelAdmin):
    list_display = ('geoservice', 'check_at', 'check_duration', 'cumulative_status',
                    'error_type', 'error_text', 'http_code', 'http_response', )
    readonly_fields = ('geoservice', 'check_at', 'check_duration', 'cumulative_status',
                    'error_type', 'error_text', 'http_code', 'http_response', )



