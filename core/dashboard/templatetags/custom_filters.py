import json
from django import template
from decimal import Decimal
register = template.Library()


@register.filter
def json_encode(value):
    if value is None:
        return ''
    if isinstance(value, Decimal):
        return float(value)
    return json.dumps(value)
