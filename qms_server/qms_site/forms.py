from django.forms import ModelForm

from qms_core.models import TmsService, WmsService, WfsService, GeoJsonService

EXCLUDE_FIELDS = ['guid', 'submitter', 'created_at', 'updated_at',]


class BaseServiceForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(BaseServiceForm, self).__init__(auto_id=self.obj_type + '_id_%s', *args, **kwargs)


class TmsForm(BaseServiceForm):
    associated_template = 'edit_snippets/tms_service.html'
    obj_type = "TMS"

    class Meta:
        model = TmsService
        exclude = EXCLUDE_FIELDS


class WmsForm(BaseServiceForm):
    associated_template = 'edit_snippets/wms_service.html'
    obj_type = "WMS"

    class Meta:
        model = WmsService
        exclude = EXCLUDE_FIELDS


class WfsForm(BaseServiceForm):
    associated_template = 'edit_snippets/wfs_service.html'
    obj_type = "WFS"

    class Meta:
        model = WfsService
        exclude = EXCLUDE_FIELDS


class GeoJsonForm(BaseServiceForm):
    associated_template = 'edit_snippets/geojson_service.html'
    obj_type = "GeoJSON"

    class Meta:
        model = GeoJsonService
        exclude = EXCLUDE_FIELDS
