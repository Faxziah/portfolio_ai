import json
from rest_framework.renderers import JSONRenderer


class UnicodeJSONRenderer(JSONRenderer):
    """JSON renderer that preserves Unicode characters (emojis, etc.)"""
    
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return b''
        
        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)
        
        if indent is None:
            separators = (',', ':')
        else:
            separators = (',', ': ')
        
        ret = json.dumps(
            data,
            cls=self.encoder_class,
            ensure_ascii=False,
            allow_nan=not self.strict,
            indent=indent,
            separators=separators
        )
        
        return ret.encode('utf-8')


