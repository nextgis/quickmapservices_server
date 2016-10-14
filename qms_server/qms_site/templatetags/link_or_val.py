from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def link_or_val(value, arg):
    """If not value, use given default."""
    if not value:
        return arg
    link = '<a target="_blank" href="{0}">{0}</a>'.format(value)
    return mark_safe(link)
