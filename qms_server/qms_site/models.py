from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from qms_core.models import NextgisUser, GeoService


class ReportType:
    SERVICE_NOT_WORKING = 'service_not_working'
    LICENSE_VIOLATION = 'license_violation'
    OTHER_PROBLEM = 'other_problem'
    GENERAL_FEEDBACK = 'general_feedback'

    choices = {
        GENERAL_FEEDBACK: _('General feedback'),
        SERVICE_NOT_WORKING: _('Service not working'),
        LICENSE_VIOLATION: _('License violation'),
        OTHER_PROBLEM: _('Other'),
    }


@python_2_unicode_compatible
class UserReport(models.Model):

    reported = models.ForeignKey(NextgisUser, on_delete=models.SET_NULL, to_field='nextgis_guid', blank=True, null=True)
    reported_email = models.EmailField(blank=True, null=True)

    geo_service = models.ForeignKey(GeoService, blank=False, null=False, on_delete=models.DO_NOTHING)

    report_type = models.CharField(max_length=20, choices=ReportType.choices.items(), null=False, blank=False)
    report_message = models.TextField(blank=True, null=True)

    report_dt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'%s %s' % (self.report_dt, self.reported_email or self.reported)