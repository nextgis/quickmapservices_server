from django.http import JsonResponse
from django.views.defaults import bad_request
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from qms_core.models import GeoService
from qms_site.forms import TmsForm, WmsForm, WfsForm, GeoJsonForm
from django.utils.translation import gettext_lazy as _

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


class CreateServiceView(TemplateView):
    template_name = 'create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateServiceView, self).get_context_data(**kwargs)
        forms = {
            TmsForm.__name__: TmsForm(),
            WmsForm.__name__: WmsForm(),
            WfsForm.__name__: WfsForm(),
            GeoJsonForm.__name__: GeoJsonForm()
        }

        context['forms'] = forms

        return context

    def post(self, request, *args, **kwargs):

        form_class_name = request.POST.get('service_type', None)

        if not form_class_name:
            return bad_request(request, _('Invalid form param: service_type'))

        if form_class_name not in (TmsForm.__name__, WmsForm.__name__, WfsForm.__name__, GeoJsonForm.__name__):
            return bad_request(request, _('Invalid form param: service_type'))

        form_class = globals()[form_class_name]
        form = form_class(**self.get_form_kwargs())

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def get_form_kwargs(self):
        kwargs = {}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        return JsonResponse({'status': 'valid'})

    def form_invalid(self, form):
        return JsonResponse({'status': 'invalid', 'errors': form.errors})
