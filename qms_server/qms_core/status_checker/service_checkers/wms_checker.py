#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from owslib.wms import WebMapService
from requests.exceptions import HTTPError, Timeout

from qms_core.models import CumulativeStatus, CheckStatusErrorType
from ..check_result import CheckResult
from .baseservice_checker import BaseServiceChecker


class WmsChecker(BaseServiceChecker):

    def check(self):
        result = CheckResult(geoservice_id=self.service.id,
                             geoservice_name=self.service.name,
                             geoservice_type=self.service.type)

        startTime = datetime.datetime.utcnow()

        try:
            wms_service = WebMapService(self.service.url, timeout=self.timeout)

            layers = self.service.layers.split(',')

            checked_layers_count = 0
            for layer in layers:
                if layer in wms_service.contents:
                    checked_layers_count += 1

            if checked_layers_count == len(layers):
                result.cumulative_status = CumulativeStatus.WORKS

            elif 0 < checked_layers_count < len(layers):
                result.cumulative_status = CumulativeStatus.PROBLEMATIC
                result.error_type = CheckStatusErrorType.MISSING_LAYER
                result.error_text = "Service supports not all layers"

            else:
                result.cumulative_status = CumulativeStatus.FAILED
                result.error_type = CheckStatusErrorType.MISSING_LAYER
                result.error_text = "No one layer was found"

        except AttributeError as error:
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_type = CheckStatusErrorType.INVALID_RESPONSE
            result.error_text = u'Not WMS service: ' + unicode(error)

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




