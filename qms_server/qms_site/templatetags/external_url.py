from django import template
register = template.Library()

external_links = {
    'nextgis_online': 'http://online.nextgis.com',
    'nextgis_com': 'http://nextgis.ru/en',
    'nextgis_com_ru': 'http://nextgis.ru',
    'my_nextgis': 'https://my.nextgis.com',

    'terms_ru': 'http://nextgis.ru/terms/',
    'terms_en': 'http://nextgis.ru/en/terms/',

    'privacy_ru': ' http://nextgis.ru/privacy',
    'privacy_en': ' http://nextgis.ru/en/privacy',
}


@register.simple_tag
def external_url(url_name):
    return external_links[url_name] if url_name in external_links.keys() else ''
