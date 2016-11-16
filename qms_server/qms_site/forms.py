from django.forms import ModelForm

from qms_core.models import TmsService, WmsService, WfsService, GeoJsonService

EXCLUDE_FIELDS = ['guid', 'submitter', 'created_at', 'updated_at',]

class TmsForm(ModelForm):
    associated_template = 'edit_snippets/tms_service.html'

    class Meta:
        model = TmsService
        exclude = EXCLUDE_FIELDS


class WmsForm(ModelForm):
    associated_template = 'edit_snippets/wms_service.html'

    class Meta:
        model = WmsService
        exclude = EXCLUDE_FIELDS


class WfsForm(ModelForm):
    associated_template = 'edit_snippets/wfs_service.html'

    class Meta:
        model = WfsService
        exclude = EXCLUDE_FIELDS


class GeoJsonForm(ModelForm):
    associated_template = 'edit_snippets/geojson_service.html'

    class Meta:
        model = GeoJsonService
        exclude = EXCLUDE_FIELDS
