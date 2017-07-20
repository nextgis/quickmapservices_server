#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from owslib.wfs import WebFeatureService
from requests.exceptions import HTTPError, Timeout

from qms_core.models import CumulativeStatus, CheckStatusErrorType
from ..check_result import CheckResult
from .baseservice_checker import BaseServiceChecker


class WfsChecker(BaseServiceChecker):

    def check(self):

        result = CheckResult(geoservice_id=self.service.id,
                             geoservice_name=self.service.name,
                             geoservice_type=self.service.type)

        startTime = datetime.datetime.utcnow()

        try:
            wfs_service = WebFeatureService(self.service.url, timeout=self.timeout)

            if self.service.layer in wfs_service.contents:
                result.cumulative_status = CumulativeStatus.WORKS
            else:
                result.cumulative_status = CumulativeStatus.PROBLEMATIC
                result.error_type = CheckStatusErrorType.MISSING_LAYER
                result.error_text = u'Service doesn\'t support layer {layer}'.format(layer=self.service.layer)

        except AttributeError as error:
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_type = CheckStatusErrorType.INVALID_RESPONSE
            result.error_text = u'Not WFS service: ' + unicode(error)

        # если requests вернул код ошибки веб-сервера
        except HTTPError as error:
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_text = unicode(error)

        except Timeout as error:
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_type = CheckStatusErrorType.TIMEOUT_ERROR

        except Exception as error:
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_text = unicode(error)

        duration_time = datetime.datetime.utcnow() - startTime
        result.check_duration = duration_time.total_seconds()

        return result
