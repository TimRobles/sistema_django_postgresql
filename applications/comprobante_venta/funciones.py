from applications.datos_globales import funciones
from django.contrib.contenttypes.models import ContentType
import requests, json
from applications.datos_globales.models import NubefactRespuesta

from applications.funciones import igv, numero_espacio
from applications.importaciones import registro_guardar_user

def subir_nubefact(obj, data, ruta, token, user):
    try:
        obj_nubefact = NubefactRespuesta.objects.create(
            content_type = ContentType.objects.get_for_model(obj),
            id_registro = obj.id,
            envio = data,
            created_by = user,
            updated_by = user,
        )
        headers = {"Authorization" : token, 'content-type': 'application/json'}
        r = requests.post(url=ruta, data=json.dumps(data), headers=headers)
        respuesta = r.json()
        try:
            if respuesta['aceptada_por_sunat']:
                aceptado = True
                error = False
            else:
                aceptado = False
                error = False
        except:
            aceptado = False
            error = True

        obj_nubefact.aceptado = aceptado
        obj_nubefact.error = error
        obj_nubefact.respuesta = respuesta
        registro_guardar_user(obj_nubefact, user)
        obj_nubefact.save()
        return obj_nubefact

    except Exception as e:
        print(e)
        return None


def boleta_nubefact(obj, user):
    tipo_de_comprobante = obj.tipo_comprobante
    serie = obj.serie_comprobante.serie
    numero = obj.numero_boleta
    sunat_transaction = obj.confirmacion.sunat_transaction
    cliente_tipo_de_documento = obj.cliente.tipo_documento
    cliente_numero_de_documento = obj.cliente.numero_documento
    cliente_denominacion = obj.cliente.razon_social
    cliente_direccion = obj.cliente.direccion_fiscal
    correos = obj.cliente.CorreoCliente_cliente.filter(estado=1)
    fecha_de_emision = obj.fecha_emision.strftime("%d-%m-%Y")
    fecha_de_vencimiento = obj.fecha_vencimiento.strftime("%d-%m-%Y")
    moneda = obj.moneda.nubefact
    tipo_de_cambio = numero_espacio(obj.tipo_cambio.venta)
    porcentaje_de_igv = numero_espacio(igv(obj.fecha_emision)*100)
    descuento_global = numero_espacio(obj.descuento_global)
    total_descuento = numero_espacio(obj.total_descuento)
    total_anticipo = numero_espacio(obj.total_anticipo)
    total_gravada = numero_espacio(obj.total_gravada)
    total_inafecta = numero_espacio(obj.total_inafecta)
    total_exonerada = numero_espacio(obj.total_exonerada)
    total_igv = numero_espacio(obj.total_igv)
    total_gratuita = numero_espacio(obj.total_gratuita)
    total_otros_cargos = numero_espacio(obj.total_otros_cargos)
    total = numero_espacio(obj.total)
    percepcion_tipo = numero_espacio(obj.percepcion_tipo)
    percepcion_base_imponible = numero_espacio(obj.percepcion_base_imponible)
    total_percepcion = numero_espacio(obj.total_percepcion)
    total_incluido_percepcion = numero_espacio(obj.total_incluido_percepcion)
    total_impuestos_bolsas = numero_espacio(obj.total_impuestos_bolsas)
    detraccion = numero_espacio(obj.detraccion)
    observaciones = obj.observaciones
    documento_que_se_modifica_tipo = ''
    documento_que_se_modifica_serie = ''
    documento_que_se_modifica_numero = ''
    tipo_de_nota_de_credito = ''
    tipo_de_nota_de_debito = ''
    enviar_automaticamente_a_la_sunat = True
    if len(correos)>0:
        enviar_automaticamente_al_cliente = True
    else:
        enviar_automaticamente_al_cliente = False
    condiciones_de_pago = obj.condiciones_pago
    if obj.tipo_venta == 1:
        medio_de_pago = obj.condiciones_pago
    else:
        medio_de_pago = 'credito'
    placa_vehiculo = ''
    orden_compra_servicio = ''
    if hasattr(obj.confirmacion, 'ConfirmacionOrdenCompra_confirmacion_venta'):
        orden_compra_servicio = obj.confirmacion.ConfirmacionOrdenCompra_confirmacion_venta.numero_orden
    formato_de_pdf = 'A4'
    generado_por_contingencia = obj.serie_comprobante.contingencia
    productos = obj.detalles
    guias = obj.guias
    cuotas = obj.cuotas
    data = funciones.generarDocumento(tipo_de_comprobante, serie, numero, sunat_transaction, cliente_tipo_de_documento, cliente_numero_de_documento, cliente_denominacion, cliente_direccion, correos, fecha_de_emision, fecha_de_vencimiento, moneda, tipo_de_cambio, porcentaje_de_igv, descuento_global, total_descuento, total_anticipo, total_gravada, total_inafecta, total_exonerada, total_igv, total_gratuita, total_otros_cargos, total, percepcion_tipo, percepcion_base_imponible, total_percepcion, total_incluido_percepcion, total_impuestos_bolsas, detraccion, observaciones, documento_que_se_modifica_tipo, documento_que_se_modifica_serie, documento_que_se_modifica_numero, tipo_de_nota_de_credito, tipo_de_nota_de_debito, enviar_automaticamente_a_la_sunat, enviar_automaticamente_al_cliente, condiciones_de_pago, medio_de_pago, placa_vehiculo, orden_compra_servicio, formato_de_pdf, generado_por_contingencia, productos, guias, cuotas)

    acceso_nubefact = obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.envio(obj.sociedad, ContentType.objects.get_for_model(obj))
    ruta = acceso_nubefact.acceso.ruta
    token = acceso_nubefact.acceso.token
    respuesta_nubefact = subir_nubefact(obj, data, ruta, token, user)
    return respuesta_nubefact


def factura_nubefact(obj, user):
    try:
        tipo_de_comprobante = obj.tipo_comprobante
        serie = obj.serie_comprobante.serie
        numero = obj.numero_factura
        sunat_transaction = obj.confirmacion.sunat_transaction
        cliente_tipo_de_documento = obj.cliente.tipo_documento
        cliente_numero_de_documento = obj.cliente.numero_documento
        cliente_denominacion = obj.cliente.razon_social
        cliente_direccion = obj.cliente.direccion_fiscal
        correos = obj.cliente.CorreoCliente_cliente.filter(estado=1)
        fecha_de_emision = obj.fecha_emision.strftime("%d-%m-%Y")
        fecha_de_vencimiento = obj.fecha_vencimiento.strftime("%d-%m-%Y")
        moneda = obj.moneda.nubefact
        tipo_de_cambio = numero_espacio(obj.tipo_cambio.venta)
        porcentaje_de_igv = numero_espacio(igv(obj.fecha_emision)*100)
        descuento_global = numero_espacio(obj.descuento_global)
        total_descuento = numero_espacio(obj.total_descuento)
        total_anticipo = numero_espacio(obj.total_anticipo)
        total_gravada = numero_espacio(obj.total_gravada)
        total_inafecta = numero_espacio(obj.total_inafecta)
        total_exonerada = numero_espacio(obj.total_exonerada)
        total_igv = numero_espacio(obj.total_igv)
        total_gratuita = numero_espacio(obj.total_gratuita)
        total_otros_cargos = numero_espacio(obj.total_otros_cargos)
        total = numero_espacio(obj.total)
        percepcion_tipo = numero_espacio(obj.percepcion_tipo)
        percepcion_base_imponible = numero_espacio(obj.percepcion_base_imponible)
        total_percepcion = numero_espacio(obj.total_percepcion)
        total_incluido_percepcion = numero_espacio(obj.total_incluido_percepcion)
        total_impuestos_bolsas = numero_espacio(obj.total_impuestos_bolsas)
        detraccion = numero_espacio(obj.detraccion)
        observaciones = obj.observaciones
        documento_que_se_modifica_tipo = ''
        documento_que_se_modifica_serie = ''
        documento_que_se_modifica_numero = ''
        tipo_de_nota_de_credito = ''
        tipo_de_nota_de_debito = ''
        enviar_automaticamente_a_la_sunat = True
        if len(correos)>0:
            enviar_automaticamente_al_cliente = True
        else:
            enviar_automaticamente_al_cliente = False
        condiciones_de_pago = obj.condiciones_pago
        if obj.tipo_venta == 1:
            medio_de_pago = obj.condiciones_pago
        else:
            medio_de_pago = 'credito'
        placa_vehiculo = ''
        orden_compra_servicio = ''
        if hasattr(obj.confirmacion, 'ConfirmacionOrdenCompra_confirmacion_venta'):
            orden_compra_servicio = obj.confirmacion.ConfirmacionOrdenCompra_confirmacion_venta.numero_orden
        formato_de_pdf = 'A4'
        generado_por_contingencia = obj.serie_comprobante.contingencia
        productos = obj.detalles
        guias = obj.guias
        cuotas = obj.cuotas
        data = funciones.generarDocumento(tipo_de_comprobante, serie, numero, sunat_transaction, cliente_tipo_de_documento, cliente_numero_de_documento, cliente_denominacion, cliente_direccion, correos, fecha_de_emision, fecha_de_vencimiento, moneda, tipo_de_cambio, porcentaje_de_igv, descuento_global, total_descuento, total_anticipo, total_gravada, total_inafecta, total_exonerada, total_igv, total_gratuita, total_otros_cargos, total, percepcion_tipo, percepcion_base_imponible, total_percepcion, total_incluido_percepcion, total_impuestos_bolsas, detraccion, observaciones, documento_que_se_modifica_tipo, documento_que_se_modifica_serie, documento_que_se_modifica_numero, tipo_de_nota_de_credito, tipo_de_nota_de_debito, enviar_automaticamente_a_la_sunat, enviar_automaticamente_al_cliente, condiciones_de_pago, medio_de_pago, placa_vehiculo, orden_compra_servicio, formato_de_pdf, generado_por_contingencia, productos, guias, cuotas)

        acceso_nubefact = obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.envio(obj.sociedad, ContentType.objects.get_for_model(obj))
        ruta = acceso_nubefact.acceso.ruta
        token = acceso_nubefact.acceso.token
        respuesta_nubefact = subir_nubefact(obj, data, ruta, token, user)
        return respuesta_nubefact
    except Exception as e:
        print("**************************")
        print(e)
        print("**************************")
        return None


def anular_nubefact(obj, user):
    tipo_de_comprobante = obj.tipo_comprobante
    serie = obj.serie_comprobante.serie
    if hasattr(obj, 'numero_boleta'):
        numero = obj.numero_boleta
    elif hasattr(obj, 'numero_factura'):
        numero = obj.numero_factura
    motivo = obj.motivo_anulacion
    data = funciones.anularDocumento(tipo_de_comprobante, serie, numero, motivo)

    acceso_nubefact = obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.envio(obj.sociedad, ContentType.objects.get_for_model(obj))
    ruta = acceso_nubefact.acceso.ruta
    token = acceso_nubefact.acceso.token
    respuesta_nubefact = subir_nubefact(obj, data, ruta, token, user)
    return respuesta_nubefact
