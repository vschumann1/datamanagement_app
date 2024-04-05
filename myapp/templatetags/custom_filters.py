from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

register = template.Library()

@register.filter(name='get_field_value')
def get_field_value(instance, field_name):
    """Retrieves the value of a model instance field dynamically."""
    return getattr(instance, field_name, '')


register = template.Library()

@register.filter(is_safe=True)  # Ensure your filter is marked as safe if it returns safe HTML/text
def intdot(value):
    try:
        # Handle value if it's a float
        if isinstance(value, float):
            value = round(value)  # You can also use int(value) if you're sure you won't need rounding
    except (ValueError, TypeError):
        return value  # If conversion fails, return original value
    value_with_comma = intcomma(value)
    return value_with_comma.replace(',', '.')



@register.filter(name='get_field_value')
def get_field_value(item, field_name):
    return getattr(item, field_name, "N/A")
