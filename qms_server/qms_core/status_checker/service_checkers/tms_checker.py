#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import datetime

import requests
import logging
from requests.exceptions import HTTPError, Timeout

from qms_core.models import CumulativeStatus, CheckStatusErrorType
from ..check_result import CheckResult
from .baseservice_checker import BaseServiceChecker
import math

class TmsChecker(BaseServiceChecker):

    def deg2num(self, lat_deg, lon_deg, zoom):
      lat_rad = math.radians(lat_deg)
      n = 2.0 ** zoom
      xtile = int((lon_deg + 180.0) / 360.0 * n)
      ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
      return (xtile, ytile)

    def __generate_alt_urls(self, tms_service):
        url_pattern, subdomains = tms_service.get_url_pattern_and_subdomains()
        urls = []
        for subdomain in subdomains:
            urls.append(
                url_pattern % {'subdomain': subdomain}
            )
        return urls

    def __generate_url(self, tms_service):
        alt_urls = self.__generate_alt_urls(tms_service)
        if alt_urls:
            tms_url = alt_urls[random.randint(0, len(alt_urls)-1)]
        else:
            tms_url = tms_service.url

        return tms_url

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
        result.cumulative_status = CumulativeStatus.FAILED
        result.error_text = ''

        startTime = datetime.datetime.utcnow()
        try:
            extent_center = self.service.extent.centroid if self.service.extent else None
            x, y = 0, 0
            tms_url = self.__generate_url(self.service)
            
            if self.service.z_min is not None:
                if extent_center:
                    x, y = self.deg2num(extent_center.y, extent_center.x, self.service.z_min)
                test_url = tms_url.format(z=self.service.z_min, x=x, y=y)
            elif self.service.z_max is not None:
                if extent_center:
                    x, y = self.deg2num(extent_center.y, extent_center.x, self.service.z_max)
                test_url = tms_url.format(z=self.service.z_max, x=x, y=y)
            else:
                # test_url = None
                # result.cumulative_status = CumulativeStatus.FAILED
                # result.error_text = 'Not set z_min and z_max for TMS'

                # Try 0 0 0 tile now
                if extent_center:
                    x, y = self.deg2num(extent_center.y, extent_center.x, 0)
                test_url = tms_url.format(z=0, x=x, y=y)

            if test_url:
                response = requests.get(test_url, timeout=self.timeout)
                str_status_http = f'{response.status_code}'
                content_type = response.headers['content-type']

                result.http_code = response.status_code

                # пока просто если сервис вернул картинку, то считаем, что сервис работает
                # можно добавить проверку на пустую картинку
                if response.status_code == 200:
                    if content_type == 'image/png' or content_type == 'image/jpeg':
                        result.cumulative_status = CumulativeStatus.WORKS
                        str_status_whole = 'GREEN'
                    else:
                        result.cumulative_status = CumulativeStatus.PROBLEMATIC
                        str_status_whole = 'YELLOW'
                        result.error_type = CheckStatusErrorType.INVALID_RESPONSE
                        result.error_text = 'service response is not image'
                else:
                    result.cumulative_status = CumulativeStatus.PROBLEMATIC
                    str_status_whole = 'YELLOW'
                    result.error_text = 'Non 200 http code'
                    result.http_response = response.text
                    result.error_type = CheckStatusErrorType.INVALID_RESPONSE
            str_status_exception = ''
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

            duration_seconds = duration_time.total_seconds()
            duration_seconds = "%.2f" % duration_seconds
            str_log = f'[{_id} {_type}] [{str_status_whole}] {duration_seconds} sec: http: ' \
                      f'{str_status_http} {str_status_exception} {str_exception_type} {str_exception_name}'
            logger.info(str_log)

        return result
