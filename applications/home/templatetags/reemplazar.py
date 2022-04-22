from django import template

register = template.Library()

@register.filter
def espacio_guion(value):
    return value.replace(" ","-").lower()