from django.utils.six import BytesIO
from imagekit.generatorlibrary import Thumbnail
from rest_framework.renderers import BaseRenderer, JSONRenderer


class DefaultRenderingParams:
    min_size = 16
    max_size = 64

    def __init__(self):
        self.width = 32
        self.height = 32

class IconRenderer(BaseRenderer):
    media_type = 'image/png'
    format = 'png'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if isinstance(data, dict) or isinstance(data, str):
            return self._render_json(data, accepted_media_type, renderer_context)

        params = self._parse_query_params(renderer_context)

        image_generator = Thumbnail(source=data, width=params.width, height=params.height, upscale=True)
        image_generator.format = 'png'

        result = image_generator.generate()

        return result.read()

    def _parse_query_params(self, renderer_context):
        params = DefaultRenderingParams()

        if renderer_context and 'request' in renderer_context and renderer_context['request']:
            width = renderer_context['request'].query_params.get('width', None)
            if width:
                try:
                    width = int(width)
                    if DefaultRenderingParams.min_size <= width <= DefaultRenderingParams.max_size:
                        params.width = width
                except:
                    pass
            height = renderer_context['request'].query_params.get('height', None)
            if height:
                try:
                    height = int(height)
                    if DefaultRenderingParams.min_size <= height <= DefaultRenderingParams.max_size:
                        params.height = height
                except:
                    pass

        return params


    def _render_json(self, data, accepted_media_type=None, renderer_context=None):
        return JSONRenderer().render(data, accepted_media_type, renderer_context)
