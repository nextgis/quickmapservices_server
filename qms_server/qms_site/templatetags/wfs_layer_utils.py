from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def wfs_layer_name(full_layer_name):
    return full_layer_name.split(':')[1] if ':' in full_layer_name else full_layer_name

@register.filter
@stringfilter
def wfs_layer_namespace(full_layer_name):
    return full_layer_name.split(':')[0] if ':' in full_layer_name else None
