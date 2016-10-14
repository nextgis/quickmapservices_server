from django import template

register = template.Library()


@register.filter(is_safe=False)
def default_if_not(value, arg):
    """If not value, use given default."""
    if not value:
        return arg
    return value
