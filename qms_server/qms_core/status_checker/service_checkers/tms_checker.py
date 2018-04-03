#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import datetime

import requests
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
        result = CheckResult(geoservice_id=self.service.id,
                             geoservice_name=self.service.name,
                             geoservice_type=self.service.type)

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
                content_type = response.headers['content-type']

                result.http_code = response.status_code

                # пока просто если сервис вернул картинку, то считаем, что сервис работает
                # можно добавить проверку на пустую картинку
                if response.status_code == 200:
                    if content_type == 'image/png' or content_type == 'image/jpeg':
                        result.cumulative_status = CumulativeStatus.WORKS
                    else:
                        result.cumulative_status = CumulativeStatus.PROBLEMATIC
                        result.error_type = CheckStatusErrorType.INVALID_RESPONSE
                        result.error_text = 'service response is not image'
                else:
                    result.cumulative_status = CumulativeStatus.PROBLEMATIC
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
