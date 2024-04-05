from django import template

register = template.Library()

@register.simple_tag
def get_fields(obj):
    return obj._meta.get_fields()
