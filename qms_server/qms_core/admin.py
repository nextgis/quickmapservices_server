from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _
from qms_core.models import NextgisUser, GeoService, TmsService, WmsService, WfsService, ServiceIcon, GeoJsonService, \
    GeoServiceStatus


@admin.register(NextgisUser)
class NextgisUserAdmin(UserAdmin):

    service_readonly_fields = ('nextgis_id', 'nextgis_guid',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('NextGIS ID'), {'fields': ('nextgis_id', 'nextgis_guid',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(GeoService)
class GeoServiceAdmin(admin.ModelAdmin):
    readonly_fields = (
        'id', 'guid', 'name', 'desc', 'type', 'epsg', 'icon',
        'license_name', 'license_url', 'copyright_text', 'copyright_url', 'terms_of_use_url',
        'submitter', 'created_at', 'updated_at', 'source', 'source_url',
        'cumulative_status', 'last_status'
    )

    list_display = ('id', 'type', 'name', 'desc', 'cumulative_status', )
    list_filter = ('type',)
    search_fields = ('name', 'desc')

    def cumulative_status(self, obj):
        return obj.last_status.cumulative_status if obj.last_status else obj.last_status

    cumulative_status.admin_order_field = 'last_status__cumulative_status'
    cumulative_status.admin_filter_field = 'last_status__cumulative_status'
    cumulative_status.short_description = 'Cumulative status'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False



service_readonly_fields = ('guid', 'type',)
common_fieldset = (_('Common'), {'fields': ('guid', 'type', 'name', 'desc', 'epsg', 'icon')})
license_fieldset = (_('License & Copyright'), {'fields': ('license_name', 'license_url', 'copyright_text', 'copyright_url', 'terms_of_use_url')})
source_fieldset = (_('Source info'), {'fields': ('source', 'source_url')})
common_list_display = ('id', 'name', 'desc')


@admin.register(TmsService)
class TmsServiceAdmin(admin.ModelAdmin):
    readonly_fields = service_readonly_fields
    list_display = common_list_display
    search_fields = ('name', 'desc')

    fieldsets = (
        common_fieldset,
        license_fieldset,
        source_fieldset,
        (_('TMS'), {'fields': ('url', 'z_min', 'z_max', 'y_origin_top')}),
    )


@admin.register(WmsService)
class WmsServiceAdmin(admin.ModelAdmin):
    readonly_fields = service_readonly_fields
    list_display = common_list_display
    search_fields = ('name', 'desc')

    fieldsets = (
        common_fieldset,
        license_fieldset,
        source_fieldset,
        (_('WMS'), {'fields': ('url', 'params', 'layers', 'turn_over', 'format')}),
    )


@admin.register(WfsService)
class WfsServiceAdmin(admin.ModelAdmin):
    readonly_fields = service_readonly_fields
    list_display = common_list_display
    search_fields = ('name', 'desc')

    fieldsets = (
        common_fieldset,
        license_fieldset,
        source_fieldset,
        (_('WFS'), {'fields': ('url', 'layer')}),
    )


@admin.register(GeoJsonService)
class GeoJsonServiceAdmin(admin.ModelAdmin):
    readonly_fields = service_readonly_fields
    list_display = common_list_display
    search_fields = ('name', 'desc')

    fieldsets = (
        common_fieldset,
        license_fieldset,
        source_fieldset,
        (_('GeoJSON'), {'fields': ('url', )}),
    )


@admin.register(ServiceIcon)
class ServiceIconAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', )


@admin.register(GeoServiceStatus)
class GeoServiceStatusAdmin(admin.ModelAdmin):
    list_display = ('geoservice', 'check_at', 'check_duration', 'cumulative_status',
                    'http_code', 'http_response', 'error_type', 'error_text')



