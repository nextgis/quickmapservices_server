#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import logging
from owslib.wfs import WebFeatureService
from requests.exceptions import HTTPError, Timeout

from qms_core.models import CumulativeStatus, CheckStatusErrorType
from ..check_result import CheckResult
from .baseservice_checker import BaseServiceChecker


class WfsChecker(BaseServiceChecker):

    def check(self):
        logger = logging.getLogger('qms_checking')
        str_status_exception = 'EXCEPTION! '
        str_status_whole = 'RED'
        str_exception_type = ''
        str_exception_name = ''
        result = CheckResult(geoservice_id=self.service.id,
                             geoservice_name=self.service.name,
                             geoservice_type=self.service.type)

        startTime = datetime.datetime.utcnow()

        try:
            wfs_service = WebFeatureService(self.service.url, timeout=self.timeout)

            if self.service.layer in wfs_service.contents:
                result.cumulative_status = CumulativeStatus.WORKS
                str_status_whole = 'GREEN'
            else:
                result.cumulative_status = CumulativeStatus.PROBLEMATIC
                str_status_whole = 'YELLOW'
                result.error_type = CheckStatusErrorType.MISSING_LAYER
                result.error_text = u'Service doesn\'t support layer {layer}'.format(layer=self.service.layer)
            str_status_exception = ''
        except AttributeError as error:
            str_exception_type = 'AttributeError'
            str_exception_name = str(error)
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_type = CheckStatusErrorType.INVALID_RESPONSE
            result.error_text = u'Not WFS service: ' + str(error)

        # если requests вернул код ошибки веб-сервера
        except HTTPError as error:
            str_exception_type = 'HTTPError'
            str_exception_name = str(error)
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_text = str(error)

        except Timeout as error:
            str_exception_type = 'Timeout'
            str_exception_name = str(error)
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_type = CheckStatusErrorType.TIMEOUT_ERROR

        except Exception as error:
            str_exception_type = 'Exception'
            str_exception_name = str(error)
            result.cumulative_status = CumulativeStatus.FAILED
            result.error_text = str(error)

        finally:
            _id = self.service.id
            _type = self.service.type

            duration_time = datetime.datetime.utcnow() - startTime
            result.check_duration = duration_time.total_seconds()
            duration_seconds = "%.2f" % duration_time.total_seconds()
            str_log = f'[{_id} {_type}] [{str_status_whole}] {duration_seconds} sec: ' \
                      f'{str_status_exception} {str_exception_type} {str_exception_name}'
            logger.info(str_log)

        return result
