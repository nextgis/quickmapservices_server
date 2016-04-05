from django.conf.urls import url, include

urlpatterns = [
    # Common API

    # API v1
    url(r'^v1/', include('qms_core.api.v1.urls'))
]
