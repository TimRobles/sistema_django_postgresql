from datetime import date
from decimal import Decimal
from django.contrib.auth import get_user_model
import json
import io
from time import sleep
from django.db import models
from applications.datos_globales.models import TipoCambio, TipoCambioSunat

from applications.funciones import consulta_sunat_tipo_cambio, numero_cero, numero_espacio, numero_guion, registrar_excepcion_interna, registrar_excepcion_sin_user

def generarDocumento(tipo_de_comprobante, serie, numero, sunat_transaction, cliente_tipo_de_documento, cliente_numero_de_documento, cliente_denominacion, cliente_direccion, correos, fecha_de_emision, fecha_de_vencimiento, moneda, tipo_de_cambio, porcentaje_de_igv, descuento_global, total_descuento, total_anticipo, total_gravada, total_inafecta, total_exonerada, total_igv, total_gratuita, total_otros_cargos, total, percepcion_tipo, percepcion_base_imponible, total_percepcion, total_incluido_percepcion, total_impuestos_bolsas, detraccion, observaciones, documento_que_se_modifica_tipo, documento_que_se_modifica_serie, documento_que_se_modifica_numero, tipo_de_nota_de_credito, tipo_de_nota_de_debito, enviar_automaticamente_a_la_sunat, enviar_automaticamente_al_cliente, condiciones_de_pago, medio_de_pago, placa_vehiculo, orden_compra_servicio, formato_de_pdf, generado_por_contingencia, productos, guias, cuotas):
    try:
        data = {}
        data['operacion'] = "generar_comprobante"
        data['tipo_de_comprobante'] = tipo_de_comprobante
        data["serie"] = serie
        data["numero"] = numero
        data["sunat_transaction"] = sunat_transaction
        data["cliente_tipo_de_documento"] = cliente_tipo_de_documento
        data["cliente_numero_de_documento"] = cliente_numero_de_documento
        data["cliente_denominacion"] = cliente_denominacion
        data["cliente_direccion"] = cliente_direccion
        correo1=""
        correo2=""
        correo3=""
        if len(correos)>2:
            correo1=correos[0].correo
            correo2=correos[1].correo
            correo3=correos[2].correo
        elif len(correos)==2:
            correo1=correos[0].correo
            correo2=correos[1].correo
        elif len(correos)==1:
            correo1=correos[0].correo
        data["cliente_email"] = correo1
        data["cliente_email_1"] = correo2
        data["cliente_email_2"] = correo3
        data["fecha_de_emision"] = fecha_de_emision
        data["fecha_de_vencimiento"] = fecha_de_vencimiento
        data["moneda"] = moneda
        data["tipo_de_cambio"] = tipo_de_cambio
        data["porcentaje_de_igv"] = porcentaje_de_igv
        data["descuento_global"] = descuento_global
        data["total_descuento"] = total_descuento
        data["total_anticipo"] = total_anticipo
        data["total_gravada"] = total_gravada
        data["total_inafecta"] = total_inafecta
        data["total_exonerada"] = total_exonerada
        data["total_igv"] = total_igv
        data["total_gratuita"] = total_gratuita
        data["total_otros_cargos"] = total_otros_cargos
        data["total"] = total
        data["percepcion_tipo"] = percepcion_tipo
        data["percepcion_base_imponible"] = percepcion_base_imponible
        data["total_percepcion"] = total_percepcion
        data["total_incluido_percepcion"] = total_incluido_percepcion
        data["total_impuestos_bolsas"] = total_impuestos_bolsas
        data["detraccion"] = detraccion
        data["observaciones"] = observaciones
        data["documento_que_se_modifica_tipo"] = documento_que_se_modifica_tipo
        data["documento_que_se_modifica_serie"] = documento_que_se_modifica_serie
        data["documento_que_se_modifica_numero"] = documento_que_se_modifica_numero
        data["tipo_de_nota_de_credito"] = tipo_de_nota_de_credito
        data["tipo_de_nota_de_debito"] = tipo_de_nota_de_debito
        data["enviar_automaticamente_a_la_sunat"] = enviar_automaticamente_a_la_sunat
        data["enviar_automaticamente_al_cliente"] = enviar_automaticamente_al_cliente
        data["condiciones_de_pago"] = condiciones_de_pago
        data["medio_de_pago"] = medio_de_pago
        data["placa_vehiculo"] = placa_vehiculo
        data["orden_compra_servicio"] = orden_compra_servicio
        data["formato_de_pdf"] = formato_de_pdf
        data["generado_por_contingencia"] = generado_por_contingencia
        data["items"]=[]
        for producto in productos:
            item={}
            item['unidad_de_medida'] = producto.unidad.unidad_sunat
            item["codigo"] = numero_espacio(producto.codigo_interno)
            item["codigo_producto_sunat"] = producto.codigo_producto_sunat
            item["descripcion"] = producto.descripcion_documento
            item["cantidad"] = numero_cero(producto.cantidad)
            item["valor_unitario"] = numero_cero(producto.precio_unitario_sin_igv)
            item["precio_unitario"] = numero_cero(producto.precio_unitario_con_igv)
            item["descuento"] = numero_cero(producto.descuento)
            item["subtotal"] = numero_cero(producto.sub_total)
            item["tipo_de_igv"] = numero_cero(producto.tipo_igv)
            item["igv"] = numero_cero(producto.igv)
            item["total"] = numero_cero(producto.total)
            item["anticipo_regularizacion"] = producto.anticipo_regularizacion
            if producto.anticipo_documento_serie:
                item["anticipo_documento_serie"] = numero_espacio(producto.anticipo_documento_serie.serie)
                item["anticipo_documento_numero"] = numero_espacio(producto.anticipo_documento_numero)
            else:
                item["anticipo_documento_serie"] = ""
                item["anticipo_documento_numero"] = ""
            
            data['items'].append(item)

        data["guias"]=[]
        for guia in guias:
            item={}
            item["guia_tipo"] = 1
            item["guia_serie_numero"] = "%s-%s" % (guia.serie_comprobante.serie, guia.numero_guia)

            data["guias"].append(item)

        data["venta_al_credito"]=[]
        contador = 1
        for cuota in cuotas:
            if cuota.fecha == fecha_de_emision: continue
            item={}
            item["cuota"] = contador
            item["fecha_de_pago"] = cuota.fecha.strftime("%d-%m-%Y")
            item["importe"] = numero_espacio(cuota.monto)
            
            data["venta_al_credito"].append(item)
            contador += 1
        
        return data

    except Exception as ex:
        print("**************************************************")
        print(ex)
        print("**************************************************")
        registrar_excepcion_sin_user(ex, __file__)
        return None


def anularDocumento(tipo_de_comprobante, serie, numero, motivo):
    try:
        data = {}
        data['operacion'] = "generar_anulacion"
        data['tipo_de_comprobante'] = tipo_de_comprobante
        data["serie"] = serie
        data["numero"] = numero
        data["motivo"] = motivo
        
        return data

    except Exception as ex:
        print("**************************************************")
        print(ex)
        print("**************************************************")
        registrar_excepcion_sin_user(ex, __file__)
        return None


def generarGuia(tipo_de_comprobante, serie, numero, cliente_tipo_de_documento, cliente_numero_de_documento, cliente_denominacion, cliente_direccion, correos, fecha_de_emision, observaciones, motivo_de_traslado, peso_bruto_total, numero_de_bultos, tipo_de_transporte, fecha_de_inicio_de_traslado, transportista_documento_tipo, transportista_documento_numero, transportista_denominacion, transportista_placa_numero, conductor_documento_tipo, conductor_documento_numero, conductor_nombre, conductor_apellidos, conductor_numero_licencia, punto_de_partida_ubigeo, punto_de_partida_direccion, punto_de_llegada_ubigeo, punto_de_llegada_direccion, enviar_automaticamente_a_la_sunat, enviar_automaticamente_al_cliente, formato_de_pdf, productos):
    try:
        data = {}
        data['operacion'] = "generar_guia"
        data['tipo_de_comprobante'] = tipo_de_comprobante
        data["serie"] = serie
        data["numero"] = numero
        data["cliente_tipo_de_documento"] = cliente_tipo_de_documento
        data["cliente_numero_de_documento"] = cliente_numero_de_documento
        data["cliente_denominacion"] = cliente_denominacion
        data["cliente_direccion"] = cliente_direccion
        correo1=""
        correo2=""
        correo3=""
        if len(correos)>2:
            correo1=correos[0].correo
            correo2=correos[1].correo
            correo3=correos[2].correo
        elif len(correos)==2:
            correo1=correos[0].correo
            correo2=correos[1].correo
        elif len(correos)==1:
            correo1=correos[0].correo
        data["cliente_email"] = correo1
        data["cliente_email_1"] = correo2
        data["cliente_email_2"] = correo3
        data["fecha_de_emision"] = fecha_de_emision
        data["observaciones"] = observaciones
        data["motivo_de_traslado"] = motivo_de_traslado
        data["peso_bruto_total"] = peso_bruto_total
        data["numero_de_bultos"] = numero_de_bultos
        data["peso_bruto_unidad_de_medida"] = 'KGM'
        data["tipo_de_transporte"] = tipo_de_transporte
        data["fecha_de_inicio_de_traslado"] = fecha_de_inicio_de_traslado
        data["transportista_documento_tipo"] = transportista_documento_tipo
        data["transportista_documento_numero"] = transportista_documento_numero
        data["transportista_denominacion"] = transportista_denominacion
        data["transportista_placa_numero"] = numero_espacio(transportista_placa_numero)
        data["conductor_documento_tipo"] = conductor_documento_tipo
        data["conductor_documento_numero"] = conductor_documento_numero
        data["conductor_nombre"] = conductor_nombre
        data["conductor_apellidos"] = conductor_apellidos
        data["conductor_numero_licencia"] = conductor_numero_licencia
        data["punto_de_partida_ubigeo"] = punto_de_partida_ubigeo
        data["punto_de_partida_direccion"] = punto_de_partida_direccion
        data["punto_de_llegada_ubigeo"] = punto_de_llegada_ubigeo
        data["punto_de_llegada_direccion"] = punto_de_llegada_direccion
        data["enviar_automaticamente_a_la_sunat"] = enviar_automaticamente_a_la_sunat
        data["enviar_automaticamente_al_cliente"] = enviar_automaticamente_al_cliente
        data["formato_de_pdf"] = formato_de_pdf
        data["items"]=[]
        for producto in productos:
            item={}
            item['unidad_de_medida'] = producto.unidad.unidad_sunat
            item["codigo"] = numero_guion(producto.codigo_interno)
            # item["codigo"] = numero_espacio(producto.id_registro)
            item["descripcion"] = producto.descripcion_documento
            item["cantidad"] = numero_espacio(producto.cantidad)
            
            data['items'].append(item)
        
        return data

    except Exception as ex:
        print("**************************************************")
        print(ex)
        print("**************************************************")
        registrar_excepcion_sin_user(ex, __file__)
        return None


def consultarDocumento(tipo_de_comprobante, serie, numero):
    try:
        data = {}
        data['operacion'] = "consultar_comprobante"
        data['tipo_de_comprobante'] = tipo_de_comprobante
        data["serie"] = serie
        data["numero"] = numero
        return data

    except Exception as ex:
        print("**************************************************")
        print(ex)
        print("**************************************************")
        registrar_excepcion_sin_user(ex, __file__)
        return None
        

def consultarGuia(tipo_de_comprobante, serie, numero):
    try:
        data = {}
        data['operacion'] = "consultar_guia"
        data['tipo_de_comprobante'] = tipo_de_comprobante
        data["serie"] = serie
        data["numero"] = numero
        return data

    except Exception as ex:
        print("**************************************************")
        print(ex)
        print("**************************************************")
        registrar_excepcion_sin_user(ex, __file__)
        return None


def consultarAnulacion(tipo_de_comprobante, serie, numero):
    try:
        data = {}
        data['operacion'] = "consultar_anulacion"
        data['tipo_de_comprobante'] = tipo_de_comprobante
        data["serie"] = serie
        data["numero"] = numero
        return data

    except Exception as ex:
        print("**************************************************")
        print(ex)
        print("**************************************************")
        registrar_excepcion_sin_user(ex, __file__)
        return None


def actualizarTipoCambioSunat(fecha: date, request):
    obj, created = TipoCambioSunat.objects.get_or_create(
        fecha = fecha,
    )
    if created or not obj.tipo_cambio_venta:
        respuesta = consulta_sunat_tipo_cambio(fecha)
        print(respuesta)
        try:
            venta = Decimal(respuesta['venta']).quantize(Decimal('0.001'))
            compra = Decimal(respuesta['compra']).quantize(Decimal('0.001'))
            obj.tipo_cambio_venta = venta
            obj.tipo_cambio_compra = compra
            obj.created_by = request.user
            obj.updated_by = request.user
            obj.save()
        except Exception as ex:
            print(ex)
            registrar_excepcion_sin_user(ex, __file__)
