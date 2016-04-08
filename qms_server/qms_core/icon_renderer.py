from django.utils.six import BytesIO
from rest_framework.renderers import BaseRenderer


class IconRenderer(BaseRenderer):
    media_type = "image/png"
    format = "png"

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data.read()


