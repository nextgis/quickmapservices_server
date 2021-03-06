#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

import geojson
import requests
import logging
from requests.exceptions import HTTPError, Timeout

from qms_core.models import CumulativeStatus, CheckStatusErrorType
from ..check_result import CheckResult
from .baseservice_checker import BaseServiceChecker


class GeoJsonChecker(BaseServiceChecker):

    def check(self):
        logger = logging.getLogger('qms_checking')
        str_status_exception = 'EXCEPTION! '
        str_status_http = ''
        str_status_whole = 'RED'
        str_exception_type = ''
        str_exception_name = ''
        result = CheckResult(geoservice_id=self.service.id,
                             geoservice_name=self.service.name,
                             geoservice_type=self.service.type)

        startTime = datetime.datetime.utcnow()
        try:
            response = requests.get(self.service.url, timeout=self.timeout)
            response_text = ''
            result.http_code = response.status_code
            # content-type не проверяется, вместо этого проверяем код ответа
            # и если он равен 200, то выполняем валидацию содержимого ответа на geojson
            str_status_http = f'{response.status_code}'
            if response.status_code == 200:
                #
                #   WARNING: это исправление ошибки: иногда при статусе 200 нельзя было получить response.text
                #   из-за этого проверка зависала
                #
                bin = response.content
                response_text = bin.decode("utf-8")
                # response_text = response.text

                geojson_obj = geojson.loads(response_text)
                validation = geojson.is_valid(geojson_obj)
                if validation['valid'] == 'yes':
                    result.data = response_text
                    result.cumulative_status = CumulativeStatus.WORKS
                    str_status_whole = 'GREEN'
                else:
                    result.cumulative_status = CumulativeStatus.PROBLEMATIC
                    str_status_whole = 'YELLOW'
                    result.error_text = validation['message']
                    result.error_type = CheckStatusErrorType.INVALID_RESPONSE
            else:
                result.cumulative_status = CumulativeStatus.PROBLEMATIC
                result.error_text = 'Non 200 http code'
                result.http_response = response_text
                result.error_type = CheckStatusErrorType.INVALID_RESPONSE
            str_status_exception = ''

        # если requests вернул код ошибки веб-сервера
        except HTTPError as error:
            str_exception_type = 'HTTPError'
            str_exception_name = str(error)
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_text = str(error)

        # исключение по таймауту 10 секунд
        except Timeout as error:
            str_exception_type = 'Timeout'
            str_exception_name = str(error)
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_type = CheckStatusErrorType.TIMEOUT_ERROR

        except Exception as error:
            str_exception_type = 'Timeout'
            str_exception_name = str(error)
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_text = str(error)

        finally:
            _id = self.service.id
            _type = self.service.type

            duration_time = datetime.datetime.utcnow() - startTime
            result.check_duration = duration_time.total_seconds()

            duration_seconds = duration_time.total_seconds()
            duration_seconds = "%.2f" % duration_seconds
            str_log = f'[{_id} {_type}] [{str_status_whole}] {duration_seconds} sec: http: ' \
                      f'{str_status_http} {str_status_exception} {str_exception_type} {str_exception_name}'
            logger.info(str_log)

        return result
