import json
import os
from textwrap import indent
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
def redondear(texto, decimales=2):
    try:
        return round(texto, decimales)
    except:
        return texto

@register.filter
def filename(value):
    return os.path.basename(value.file.name)

@register.filter
def numeroXn(numero, n):
    return '0'*(n-len(str(numero))) + str(numero)

@register.filter
def get_enlace_nubefact(respuesta):
    return respuesta.respuesta['enlace']

@register.filter
def get_enlace_pdf_nubefact(respuesta):
    return respuesta.respuesta['enlace_del_pdf']

@register.filter
def diccionario(respuesta):
    return respuesta.items()

@register.filter
def es_diccionario_nubefact(respuesta):
    try:
        return type(respuesta[0]) == type(dict())
    except:
        return False