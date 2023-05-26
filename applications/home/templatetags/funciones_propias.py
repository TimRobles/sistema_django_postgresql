from datetime import date
import json
import os
from textwrap import indent
from django import template
from django.utils.safestring import mark_safe

from applications.variables import DICCIONARIO_TIPO_DOCUMENTO_SUNAT

register = template.Library()

@register.filter
def espacio_guion(value):
    texto = value
    texto = texto.replace(" ","-").lower()
    texto = texto.replace("(","-").lower()
    texto = texto.replace(")","-").lower()
    return texto

@register.filter
def validar_none(value):
    if value:
        return value
    return ""

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
def diccionario_tipo_documento(value):
    return DICCIONARIO_TIPO_DOCUMENTO_SUNAT[value]

@register.filter
def filename(value):
    return os.path.basename(value.file.name)

@register.filter
def numeroXn(numero, n):
    if numero:
        return '0'*(n-len(str(numero))) + str(numero)
    return ""

@register.filter
def get_enlace_nubefact(respuesta):
    try:
        return respuesta.respuesta['enlace']
    except:
        return respuesta

@register.filter
def get_enlace_pdf_nubefact(respuesta):
    try:
        return respuesta.respuesta['enlace_del_pdf']
    except:
        return str(respuesta) + '.pdf'

@register.filter
def diccionario(respuesta):
    return respuesta.items()

@register.filter
def es_diccionario_nubefact(respuesta):
    try:
        return type(respuesta[0]) == type(dict())
    except:
        return False

@register.filter
def nombre_usuario(usuario):
    try:
        if usuario.get_full_name():
            return usuario.get_full_name()
        return usuario.username
    except:
        return usuario.username

@register.filter
def atributo(field):
    return field.field.widget.attrs['class']
    
@register.filter
def diferencia(valor, dif):
    return valor - dif
    
@register.filter
def get_diccionario(diccionario, key):
    return diccionario.get(key)
    
@register.filter
def estado_garantia(fecha):
    if (fecha - date.today()).days > 0:
        return True
    return False
