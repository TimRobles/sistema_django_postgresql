from time import sleep
from urllib.request import Request

from applications.funciones import buscar_diccionario, consulta_ruc
from applications.variables import CONDICION_SUNAT, ESTADO_SUNAT


def validar_estado_ruc(obj):
    request = Request
    request.method = 'GET'
    ruc = obj.numero_documento
    if obj.tipo_documento == '6':
        try:
            data = consulta_ruc(ruc)
            print(data)
            obj.estado_sunat = buscar_diccionario(ESTADO_SUNAT, data['estado'])
            obj.condicion_sunat = buscar_diccionario(CONDICION_SUNAT, data['condicion'])
            obj.save()
        except:
            pass