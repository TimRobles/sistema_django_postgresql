import os
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def espacio_guion(value):
    texto = value
    texto = texto.replace(" ","-").lower()
    texto = texto.replace("(","-").lower()
    texto = texto.replace(")","-").lower()
    return texto

@register.filter
def recortar_popover(texto):
    if len(str(texto))>40:
        return mark_safe("""<span data-bs-toggle="tooltip" data-bs-placement="top" title="%s">%s...</span>""" % (str(texto), str(texto)[:40]))
    else:
        return texto

@register.filter
def redondear(texto):
    try:
        return round(texto,2)
    except:
        return texto

@register.filter
def filename(value):
    return os.path.basename(value.file.name)