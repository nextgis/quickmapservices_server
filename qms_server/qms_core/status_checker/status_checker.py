from .service_checkers.wms_checker import WmsChecker
from .service_checkers.wfs_checker import WfsChecker
from .service_checkers.tms_checker import TmsChecker
from .service_checkers.geojson_checker import GeoJsonChecker
from .service_checkers.unknown_checker import UnknownChecker

from qms_core.models import WmsService, WfsService, GeoJsonService, TmsService, GeoService, GeoServiceStatus

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

    service_checker_inst = service_checker(service)

    return service_checker_inst.check()


def check_by_id(id):
    service = GeoService.objects\
        .select_related('tmsservice')\
        .select_related('wmsservice')\
        .select_related('wfsservice')\
        .select_related('geojsonservice').get(pk=id)
    service = service.get_typed_instance()

    return check(service)


def check_by_id_and_save(id):
    result = check_by_id(id)

    print result.__dict__

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