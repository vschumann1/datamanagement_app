from django import template

register = template.Library()

@register.filter(name='get_field_value')
def get_field_value(obj, field_name):
    """Custom filter to get field values safely."""
    return getattr(obj, field_name, '')
