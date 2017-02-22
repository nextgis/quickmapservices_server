from captcha.fields import ReCaptchaField
from django.forms import ModelForm
from django.utils.translation import ugettext as _

from qms_core.models import TmsService, WmsService, WfsService, GeoJsonService
from qms_site.models import UserReport

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


class AuthReportForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuthReportForm, self).__init__(*args, **kwargs)
        # fix and translate select control
        self.fields['report_type'].choices[0] = ('', '')
        self.fields['report_type'].choices = [(k, _(v)) for k, v in self.fields['report_type'].choices]
        self.fields['report_type'].widget.choices = self.fields['report_type'].choices

    class Meta:
        model = UserReport
        exclude = ['reported', 'geo_service']


class NonAuthReportForm(AuthReportForm):
    captcha = ReCaptchaField(required=True)
