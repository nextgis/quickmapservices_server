from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def link_or_val(value, arg):
    """If not value, use given default."""
    if not value:
        return arg

    link_tmpl = u'<a target="_blank" href="{0}">{0}</a>'
    if not isinstance(value, str):
        link_tmpl = link_tmpl.encode('utf-8')
    link = link_tmpl.format(value)

    return mark_safe(link)
