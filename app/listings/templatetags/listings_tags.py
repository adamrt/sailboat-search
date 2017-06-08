from urllib.parse import urlencode
from collections import OrderedDict
from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, value):
    params = request.GET.copy()
    field = 'sort'
    if field in params.keys():
        param = params['sort']
        if param.startswith('-') and param.lstrip('-') == value:
            params[field] = value
        elif param.lstrip('-') == value:
            params[field] = "-" + value
        else:
            params[field] = value
    else:
        params[field] = value
    return urlencode(OrderedDict(sorted(params.items())))
