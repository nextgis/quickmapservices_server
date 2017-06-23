
class CheckResult:

    def __init__(self, geoservice_id=None, geoservice_name=None, geoservice_type=None,
                 check_duration=0, cumulative_status=None,
                 http_code=0, http_response=None,
                 error_type=None, error_text=None
                 ):
        self.geoservice_id = geoservice_id
        self.geoservice_name = geoservice_name
        self.geoservice_type = geoservice_type

        self.check_duration = check_duration
        self.cumulative_status = cumulative_status
        self.http_code = http_code
        self.http_response = http_response
        self.error_type = error_type
        self.error_text = error_text