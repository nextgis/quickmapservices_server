from qms_core.models import CheckStatusErrorType, CumulativeStatus
from ..check_result import CheckResult
from .baseservice_checker import BaseServiceChecker

class UnknownChecker(BaseServiceChecker):

    def check(self):
        result = CheckResult(geoservice_id=self.service.id,
                             geoservice_name=self.service.name,
                             geoservice_type=self.service.type)

        result.cumulative_status = CumulativeStatus.PROBLEMATIC
        result.error_type = CheckStatusErrorType.UNSUPPORTED_SERVICE
        return result
