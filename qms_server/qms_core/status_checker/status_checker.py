from django.conf import settings

from .service_checkers.wms_checker import WmsChecker
from .service_checkers.wfs_checker import WfsChecker
from .service_checkers.tms_checker import TmsChecker
from .service_checkers.geojson_checker import GeoJsonChecker
from .service_checkers.unknown_checker import UnknownChecker

from qms_core.models import WmsService, WfsService, GeoJsonService, TmsService, GeoService, GeoServiceStatus

import logging

_checkers_mapping = {
    WmsService.service_type: WmsChecker,
    WfsService.service_type: WfsChecker,
    GeoJsonService.service_type: GeoJsonChecker,
    TmsService.service_type: TmsChecker
}


def check(service):

    if service.type in _checkers_mapping.keys():
        service_checker = _checkers_mapping[service.type]
    else:
        service_checker = UnknownChecker

    service_checker_inst = service_checker(service, settings.SERVICE_CHECK_TIMEOUT)

    return service_checker_inst.check()


def check_by_id(id):
    service = GeoService.objects\
        .select_related('tmsservice')\
        .select_related('wmsservice')\
        .select_related('wfsservice')\
        .select_related('geojsonservice').get(pk=id)
    service = service.get_typed_instance()
    result = check(service)
    return result


def check_by_id_and_save(id):
    try:
        logger = logging.getLogger('qms_checking')
        result = check_by_id(id)


        # add new service status
        status_obj = GeoServiceStatus()
        status_obj.geoservice_id = result.geoservice_id
        status_obj.check_duration = result.check_duration
        status_obj.cumulative_status = result.cumulative_status
        status_obj.http_code = result.http_code
        status_obj.http_response = result.http_response
        status_obj.error_type = result.error_type
        status_obj.error_text = result.error_text
        status_obj.save()

        # update last status
        geoservice = status_obj.geoservice.get_typed_instance()
        geoservice.last_status = status_obj
        geoservice.save()
    except Exception as e:
        str_e = str(e)
        logger.error(str_e)

