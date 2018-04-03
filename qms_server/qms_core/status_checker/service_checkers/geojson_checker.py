#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import geojson
import requests
from requests.exceptions import HTTPError, Timeout

from qms_core.models import CumulativeStatus, CheckStatusErrorType
from ..check_result import CheckResult
from .baseservice_checker import BaseServiceChecker


class GeoJsonChecker(BaseServiceChecker):

    def check(self):
        result = CheckResult(geoservice_id=self.service.id,
                             geoservice_name=self.service.name,
                             geoservice_type=self.service.type)

        startTime = datetime.datetime.utcnow()
        try:
            response = requests.get(self.service.url, timeout=self.timeout)

            result.http_code = response.status_code
            # content-type не проверяется, вместо этого проверяем код ответа
            # и если он равен 200, то выполняем валидацию содержимого ответа на geojson
            if response.status_code == 200:
                validation = geojson.is_valid(geojson.loads(response.text))
                if validation['valid'] == 'yes':
                    result.cumulative_status = CumulativeStatus.WORKS
                else:
                    result.cumulative_status = CumulativeStatus.PROBLEMATIC
                    result.error_text = validation['message']
                    result.error_type = CheckStatusErrorType.INVALID_RESPONSE
            else:
                result.cumulative_status = CumulativeStatus.PROBLEMATIC
                result.error_text = 'Non 200 http code'
                result.http_response = response.text
                result.error_type = CheckStatusErrorType.INVALID_RESPONSE

        # если requests вернул код ошибки веб-сервера
        except HTTPError as error:
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_text = unicode(error)

        # исключение по таймауту 10 секунд
        except Timeout as error:
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_type = CheckStatusErrorType.TIMEOUT_ERROR

        except Exception as error:
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_text = unicode(error)

        duration_time = datetime.datetime.utcnow() - startTime
        result.check_duration = duration_time.total_seconds()

        return result
