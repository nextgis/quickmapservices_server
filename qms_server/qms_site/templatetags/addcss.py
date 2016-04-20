from django import template
register = template.Library()


@register.filter
def addcss(field, css):
    class_old = field.field.widget.attrs.get('class', None)
    class_new = '%s %s' % (class_old, css) if class_old else css
    return field.as_widget(attrs={"class": class_new})
