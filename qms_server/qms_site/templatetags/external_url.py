from django import template
register = template.Library()

external_links = {
    'nextgis_online': 'http://online.nextgis.com',
    'terms_of_service': 'https://id.nextgis.com/info/terms_of_service',
    'privacy_policy': 'https://id.nextgis.com/info/privacy_policy',

}


@register.simple_tag
def external_url(url_name):
    return external_links[url_name] if url_name in external_links.keys() else ''
