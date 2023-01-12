from applications.datos_globales import funciones
from django.contrib.contenttypes.models import ContentType
import requests, json
from applications.datos_globales.models import NubefactRespuesta

from applications.funciones import igv, numero_cero, numero_espacio, numero_guion
from applications.home.templatetags.funciones_propias import diccionario_tipo_documento
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


def guia_nubefact(obj, user):
    try:
        tipo_de_comprobante = obj.tipo_comprobante
        serie = obj.serie_comprobante.serie
        numero = obj.numero_guia
        cliente_tipo_de_documento = obj.cliente.tipo_documento
        cliente_numero_de_documento = obj.cliente.numero_documento
        cliente_denominacion = obj.cliente.razon_social
        cliente_direccion = obj.cliente.direccion_fiscal
        correos = obj.cliente.CorreoCliente_cliente.filter(estado=1)
        fecha_de_emision = obj.fecha_emision.strftime("%d-%m-%Y")
        observaciones = obj.observaciones_totales
        motivo_de_traslado = obj.motivo_traslado
        peso_bruto_total = numero_cero(obj.peso_total)
        numero_de_bultos = numero_espacio(obj.numero_bultos)
        if obj.transportista:
            tipo_de_transporte = '01' #TRANSPORTE PÚBLICO
            transportista_documento_tipo = obj.transportista.tipo_documento
            transportista_documento_numero = obj.transportista.numero_documento
            transportista_denominacion = obj.transportista.razon_social
        else:
            tipo_de_transporte = '02' #TRANSPORTE PRIVADO
            transportista_documento_tipo = ""
            transportista_documento_numero = ""
            transportista_denominacion = ""
        fecha_de_inicio_de_traslado = obj.fecha_traslado.strftime("%d-%m-%Y")
        transportista_placa_numero = numero_espacio(obj.placa_numero)
        conductor_documento_tipo = numero_guion(obj.conductor_tipo_documento)
        conductor_documento_numero = numero_guion(obj.conductor_numero_documento)
        conductor_nombre = numero_guion(obj.conductor_nombre)
        conductor_apellidos = numero_guion(obj.conductor_apellidos)
        conductor_numero_licencia = numero_guion(obj.conductor_numero_licencia)
        punto_de_partida_ubigeo = obj.ubigeo_partida.codigo
        punto_de_partida_direccion = obj.direccion_partida
        punto_de_llegada_ubigeo = obj.ubigeo_destino.codigo
        punto_de_llegada_direccion = obj.direccion_destino
        enviar_automaticamente_a_la_sunat = True
        if len(correos)>0:
            enviar_automaticamente_al_cliente = True
        else:
            enviar_automaticamente_al_cliente = False
        formato_de_pdf = 'A4'
        productos = obj.detalles
        data = funciones.generarGuia(tipo_de_comprobante, serie, numero, cliente_tipo_de_documento, cliente_numero_de_documento, cliente_denominacion, cliente_direccion, correos, fecha_de_emision, observaciones, motivo_de_traslado, peso_bruto_total, numero_de_bultos, tipo_de_transporte, fecha_de_inicio_de_traslado, transportista_documento_tipo, transportista_documento_numero, transportista_denominacion, transportista_placa_numero, conductor_documento_tipo, conductor_documento_numero, conductor_nombre, conductor_apellidos, conductor_numero_licencia, punto_de_partida_ubigeo, punto_de_partida_direccion, punto_de_llegada_ubigeo, punto_de_llegada_direccion, enviar_automaticamente_a_la_sunat, enviar_automaticamente_al_cliente, formato_de_pdf, productos)

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
    elif hasattr(obj, 'numero_guia'):
        numero = obj.numero_guia
    motivo = obj.motivo_anulacion
    data = funciones.anularDocumento(tipo_de_comprobante, serie, numero, motivo)

    acceso_nubefact = obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.envio(obj.sociedad, ContentType.objects.get_for_model(obj))
    ruta = acceso_nubefact.acceso.ruta
    token = acceso_nubefact.acceso.token
    respuesta_nubefact = subir_nubefact(obj, data, ruta, token, user)
    return respuesta_nubefact


def consultar_documento(obj, user):
    tipo_de_comprobante = obj.tipo_comprobante
    serie = obj.serie_comprobante.serie
    if hasattr(obj, 'numero_boleta'):
        numero = obj.numero_boleta
    elif hasattr(obj, 'numero_factura'):
        numero = obj.numero_factura
    elif hasattr(obj, 'numero_guia'):
        numero = obj.numero_guia
    data = funciones.consultarDocumento(tipo_de_comprobante, serie, numero)

    acceso_nubefact = obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.envio(obj.sociedad, ContentType.objects.get_for_model(obj))
    ruta = acceso_nubefact.acceso.ruta
    token = acceso_nubefact.acceso.token
    respuesta_nubefact = subir_nubefact(obj, data, ruta, token, user)
    return respuesta_nubefact


def consultar_guia(obj, user):
    tipo_de_comprobante = obj.tipo_comprobante
    serie = obj.serie_comprobante.serie
    if hasattr(obj, 'numero_boleta'):
        numero = obj.numero_boleta
    elif hasattr(obj, 'numero_factura'):
        numero = obj.numero_factura
    elif hasattr(obj, 'numero_guia'):
        numero = obj.numero_guia
    data = funciones.consultarGuia(tipo_de_comprobante, serie, numero)

    acceso_nubefact = obj.serie_comprobante.NubefactSerieAcceso_serie_comprobante.envio(obj.sociedad, ContentType.objects.get_for_model(obj))
    ruta = acceso_nubefact.acceso.ruta
    token = acceso_nubefact.acceso.token
    respuesta_nubefact = subir_nubefact(obj, data, ruta, token, user)
    return respuesta_nubefact
