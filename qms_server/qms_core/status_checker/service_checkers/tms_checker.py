#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import requests
from requests.exceptions import HTTPError, Timeout

from qms_core.models import CumulativeStatus, CheckStatusErrorType
from ..check_result import CheckResult
from .baseservice_checker import BaseServiceChecker


class TmsChecker(BaseServiceChecker):

    def check(self):
        result = CheckResult(geoservice_id=self.service.id,
                             geoservice_name=self.service.name,
                             geoservice_type=self.service.type)

        startTime = datetime.datetime.utcnow()
        try:
            if self.service.z_min is not None:
                test_url = self.service.url.format(z=self.service.z_min, x=0, y=0)
            elif self.service.z_max is not None:
                test_url = self.service.url.format(z=self.service.z_max, x=0, y=0)
            else:
                test_url = None
                result.cumulative_status = CumulativeStatus.FAILED
                result.error_text = 'Not set z_min and z_max for TMS'

            if test_url:
                response = requests.get(test_url, timeout=10)  # TODO: move timeout
                content_type = response.headers['content-type']

                result.http_code = response.status_code

                # пока просто если сервис вернул картинку, то считаем, что сервис работает
                # можно добавить проверку на пустую картинку
                if response.status_code == 200:
                    if content_type == 'image/png' or content_type == 'image/jpeg':
                        result.cumulative_status = CumulativeStatus.WORKS
                    else:
                        result.cumulative_status = CumulativeStatus.FAILED
                        result.error_type = CheckStatusErrorType.INVALID_RESPONSE
                        result.error_text = 'service response is not image'
                else:
                    result.cumulative_status = CumulativeStatus.FAILED
                    result.error_text = 'Non 200 http code'
                    result.http_response = response.text
                    result.error_type = CheckStatusErrorType.INVALID_RESPONSE

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
