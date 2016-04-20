from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from qms_core.models import GeoService


class GeoserviceListView(TemplateView):
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        return {
            'services': GeoService.objects.all().order_by('name'),
            'body_class': 'admin'
        }


class GeoserviceDetailView(TemplateView):
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        service = get_object_or_404(GeoService.objects.select_related('tmsservice')
                                                      .select_related('wmsservice')
                                                      .select_related('wfsservice'),
                                    id=kwargs['pk'])
        return {
            'service': service,
            'body_class': 'admin'
        }
