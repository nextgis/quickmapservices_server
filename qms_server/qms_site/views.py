from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.views.defaults import bad_request
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.views.generic import UpdateView

from qms_core.models import GeoService, TmsService, WmsService, WfsService, GeoJsonService
from qms_site.forms import TmsForm, WmsForm, WfsForm, GeoJsonForm
from django.utils.translation import gettext_lazy as _

class GeoserviceListView(TemplateView):
    template_name = 'list.html'

    def get_context_data(self, **kwargs):
        return {
            'services': GeoService.objects.all().order_by('name')
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


class CreateServiceView(LoginRequiredMixin, TemplateView):
    template_name = 'create.html'
    acceptable_forms = (TmsForm.__name__, WmsForm.__name__, WfsForm.__name__, GeoJsonForm.__name__)

    def get_context_data(self, **kwargs):
        context = super(CreateServiceView, self).get_context_data(**kwargs)
        forms = {
            TmsForm.__name__: TmsForm(),
            WmsForm.__name__: WmsForm(),
            WfsForm.__name__: WfsForm(),
            GeoJsonForm.__name__: GeoJsonForm()
        }

        if 'form' in kwargs and kwargs['form'].__class__.__name__ in self.acceptable_forms:
            forms[kwargs['form'].__class__.__name__] = kwargs['form']
            if 'error_form_type' in  kwargs and kwargs['error_form_type'] in self.acceptable_forms:
                context['error_form_type'] = kwargs['error_form_type']

        context['forms'] = forms
        return context


    def post(self, request, *args, **kwargs):

        form_class_name = request.POST.get('service_type', None)

        if not form_class_name:
            return bad_request(request, _('Invalid form param: service_type'))

        if form_class_name not in self.acceptable_forms:
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
        self.object = form.save(commit=False)
        self.object.submitter = self.request.user
        self.object.save()
        return HttpResponseRedirect(reverse('site_geoservice_list'))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, error_form_type=form.__class__.__name__))



class EditServiceView(LoginRequiredMixin, UpdateView):
    template_name = 'edit.html'
    success_url = reverse_lazy('site_geoservice_list')

    queryset = GeoService.objects\
        .select_related('tmsservice')\
        .select_related('wmsservice')\
        .select_related('wfsservice')\
        .select_related('geojsonservice')


    def get_object(self, queryset=None):
        model_map = {
            TmsService.service_type: lambda x: x.tmsservice,
            WmsService.service_type: lambda x: x.wmsservice,
            WfsService.service_type: lambda x: x.wfsservice,
            GeoJsonService.service_type: lambda x: x.geojsonservice
        }
        obj = super(EditServiceView, self).get_object(queryset=queryset)

        if obj:
            return model_map[obj.type](obj)
        return obj


    def get_context_data(self, **kwargs):
        context = super(EditServiceView, self).get_context_data(**kwargs)
        context['form_name'] = context['form'].__class__.__name__
        return context


    def get_form_class(self):
        form_map = {
            TmsService.service_type: TmsForm,
            WmsService.service_type: WmsForm,
            WfsService.service_type: WfsForm,
            GeoJsonService.service_type: GeoJsonForm
        }
        obj = self.get_object()
        return form_map[obj.type]


    def get(self, request, *args, **kwargs):
        if not self.check_submitter(request):
            return HttpResponseForbidden()
        return super(EditServiceView, self).get(self, request, *args, **kwargs)


    def post(self, request, *args, **kwargs):
        if not self.check_submitter(request):
            return HttpResponseForbidden()
        return super(EditServiceView, self).post(self, request, *args, **kwargs)

    def check_submitter(self, request):
        obj = self.get_object()
        return obj.submitter == request.user
