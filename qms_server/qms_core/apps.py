from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig


class QmsCoreConfig(AppConfig):
    name = 'qms_core'
    verbose_name = _('NextGIS QMS')
