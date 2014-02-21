from django import template
register = template.Library()

@register.filter
def get_field_value(obj, field_name):
    return getattr(obj, field_name, None)

@register.filter
def get_verbose_name(obj, field_name):
    return obj._meta.get_field(field_name).verbose_name

register.tag('get_verbose_name', get_verbose_name)
register.tag('get_field_value', get_field_value)