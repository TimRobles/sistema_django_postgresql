from datetime import date, datetime
import json
import requests
from decimal import Decimal
from requests.adapters import HTTPAdapter
from django.core.exceptions import ValidationError
from urllib3.util.retry import Retry
import applications
import math
import random
import string
from applications.soporte_sistema.models import Excepcion
from django.contrib import messages
import sys

def consulta_ruc(ruc):
    token = "apis-token-1914.9jOkTIeoTyuru0Mpx4ulp40uAqojGAFP" #ConsultaRucMP1
    url = "https://api.apis.net.pe/v1/ruc?numero="
    headers = {"Authorization" : "Bearer %s" % token, 'Accept':'application/json'}
    r = requests.get(url + str(ruc), headers=headers)
    data = r.json()
    return data

# {
#     'nombre': 'TELMARK SUPPLY S.A.C. - TELMARK',
#     'tipoDocumento': '6',
#     'numeroDocumento': '20547974787',
#     'estado': 'ACTIVO',
#     'condicion': 'HABIDO',
#     'direccion': 'PZA. 27 DE NOVIEMBRE NRO 450 URB. CHACARILLA SANTA CRUZ ',
#     'ubigeo': '150131',
#     'viaTipo': 'PZA.',
#     'viaNombre': '27 DE NOVIEMBRE',
#     'zonaCodigo': 'URB.',
#     'zonaTipo': 'CHACARILLA SANTA CRUZ',
#     'numero': '450',
#     'interior': '-',
#     'lote': '-',
#     'dpto': '-',
#     'manzana': '-',
#     'kilometro': '-',
#     'distrito': 'SAN ISIDRO',
#     'provincia': 'LIMA',
#     'departamento': 'LIMA'
#     }

def consulta_dni(dni):
    token = "7c95cc7e139486c8b86f15f9d96ec096" #Libre
    url = "https://api.apifacturacion.com/dni/"
    data = {"token" : "%s" % token}

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    r = session.post(url + str(dni), data=data)
    data = r.json()
    return data

# {
#     'dni': '47834310',
#     'cliente': 'TIM ARNOLD ROBLES MARTINEZ'
#     }

def consulta_dni2(dni):
    token = "apis-token-1914.9jOkTIeoTyuru0Mpx4ulp40uAqojGAFP" #ConsultaRucMP1
    url = "https://api.apis.net.pe/v1/dni?numero="
    headers = {"Authorization" : "Bearer %s" % token, 'Accept':'application/json'}
    r = requests.get(url + str(dni), headers=headers)
    data = r.json()

    return data

# {
#  "nombre":"HUAMANI MENDOZA ERACLEO JUAN",
#  "tipoDocumento":"1",
#  "numeroDocumento":"46027897",
#  "estado":"",
#  "condicion":"",
#  "direccion":"",
#  "ubigeo":"",
#  "viaTipo":"",
#  "viaNombre":"",
#  "zonaCodigo":"",
#  "zonaTipo":"",
#  "numero":"",
#  "interior":"",
#  "lote":"",
#  "dpto":"",
#  "manzana":"",
#  "kilometro":"",
#  "distrito":"",
#  "provincia":"",
#  "departamento":"",
#  "nombres": "ERACLE JUAN",
#  "apellidoPaterno": "HUAMANI",
#  "apellidoMaterno": "MENDOZA"
#}

def consulta_sunat_tipo_cambio(fecha: date):
    token = "apis-token-1914.9jOkTIeoTyuru0Mpx4ulp40uAqojGAFP" #ConsultaRucMP1
    url = "https://api.apis.net.pe/v1/tipo-cambio-sunat?fecha="
    headers = {"Authorization" : "Bearer %s" % token, 'Accept':'application/json'}
    r = requests.get(f"{url}{fecha.year}-{numeroXn(fecha.month, 2)}-{numeroXn(fecha.day, 2)}", headers=headers)
    data = r.json()

    return data

# {
# 'compra': 3.808,
# 'venta': 3.82,
# 'origen': 'SUNAT',
# 'moneda': 'USD',
# 'fecha': '2023-01-03'
# }

def validar_texto(texto):
    lista = texto.split(" ")
    for palabra in lista:
        if not palabra.isalpha():
            raise ValidationError('%s tiene caracteres incorrectos' % texto)

def validar_numero(texto):
    for letra in texto:
        if not letra.isnumeric():
            raise ValidationError('%s tiene caracteres incorrectos' % texto)


def consulta_distancia(longitud, latitud, sede_id):
    ubicacion = applications.recepcion.models.GeoLocalizacion.objects.get(sede__id=sede_id)
    local = (float(ubicacion.longitud), float(ubicacion.latitud))
    posicion = (float(longitud), float(latitud))
    """ R = 3958.8 #Radius of the Earth in miles """
    R = 6371.0710 #Radius of the Earth in kilometers
    rlat1 = local[1] * (math.pi/180) #Convert degrees to radians
    rlat2 = posicion[1] * (math.pi/180) #Convert degrees to radians
    difflat = rlat2-rlat1 #Radian difference (latitudes)
    difflon = (posicion[0]-local[0]) * (math.pi/180) #Radian difference (longitudes)

    distancia = 2 * R * math.asin(math.sqrt(math.sin(difflat/2)*math.sin(difflat/2)+math.cos(rlat1)*math.cos(rlat2)*math.sin(difflon/2)*math.sin(difflon/2))) #Distancia en kilómetros
    if int(distancia*1000) > ubicacion.distancia:
        return "Estás a %i metros de la oficina." % int(distancia*1000)
    else:
        return "Estás en la oficina"


def slug_aleatorio(modelo):
    letters = string.ascii_uppercase
    repetir = True
    while repetir:
        slugs = []
        slugs.append(''.join(random.choice(letters) for i in range(4)))
        slugs.append(''.join(random.choice(letters) for i in range(4)))
        slugs.append(''.join(random.choice(letters) for i in range(4)))
        slugs.append(''.join(random.choice(letters) for i in range(4)))

        slug = '-'.join(slugs)
        if len(modelo.objects.filter(slug=slug))==0:
            repetir = False
    return slug


def calculos_linea(cantidad, precio_unitario_con_igv, precio_final_con_igv, valor_igv, tipo_igv, anticipo_regularizacion=False, tipo_cambio=Decimal('1')):
    respuesta = {}

    if tipo_igv==8:
        precio_unitario_sin_igv = precio_unitario_con_igv
        precio_final_sin_igv = precio_final_con_igv
    else:
        precio_unitario_sin_igv = Decimal(Decimal(precio_unitario_con_igv)/(1 + Decimal(valor_igv))).quantize(Decimal('0.0000000001'))
        precio_final_sin_igv = Decimal(Decimal(precio_final_con_igv)/(1 + Decimal(valor_igv))).quantize(Decimal('0.0000000001'))

    descuento_unitario = (precio_unitario_sin_igv - precio_final_sin_igv).quantize(Decimal('0.0000000001'))
    descuento = (descuento_unitario * Decimal(cantidad)).quantize(Decimal('0.01'))

    total = (Decimal(cantidad) * precio_final_con_igv).quantize(Decimal('0.01'))
    if tipo_igv==8:
        subtotal = total
    else:
        subtotal = (Decimal(cantidad) * precio_final_sin_igv).quantize(Decimal('0.01'))
    igv = (total - subtotal).quantize(Decimal('0.01'))

    respuesta['precio_unitario_sin_igv'] = precio_unitario_sin_igv
    respuesta['descuento'] = descuento
    respuesta['descuento_con_igv'] = (precio_unitario_con_igv * cantidad).quantize(Decimal('0.0000000001')) - total
    respuesta['subtotal'] = subtotal
    respuesta['igv'] = igv
    respuesta['total'] = total
    respuesta['tipo_igv'] = tipo_igv
    respuesta['anticipo_regularizacion'] = anticipo_regularizacion

    return respuesta


def calculos_totales(lista_resultados_linea, descuento_global_cotizacion, descuento_oferta, descuento_global, otros_cargos, valor_igv, tipo_cambio=Decimal('1')):
    respuesta = {}

    descuento_global_con_igv = (descuento_global * (1+Decimal(valor_igv))).quantize(Decimal('0.01'))

    suma_igv = Decimal('0.00')
    total_descuento = Decimal('0.00')
    total_descuento_con_igv = Decimal('0.00')
    total_gravada = Decimal('0.00')
    total_inafecta = Decimal('0.00')
    total_exonerada = Decimal('0.00')
    total_anticipo = Decimal('0.00')

    total_gratuita = Decimal('0.00')
    total_otros_cargos = otros_cargos
    total_icbper = Decimal('0.00')
    total = Decimal('0.00')
    for resultado_linea in lista_resultados_linea:
        total_descuento += resultado_linea['descuento']
        total_descuento_con_igv += resultado_linea['descuento_con_igv']
        if resultado_linea['tipo_igv']==8:
            total_exonerada += resultado_linea['subtotal']
        else:
            if resultado_linea['anticipo_regularizacion']:
                suma_igv -= resultado_linea['igv']
                total_gravada -= resultado_linea['subtotal']
                total_anticipo += resultado_linea['subtotal']
            else:
                suma_igv += resultado_linea['igv']
                total_gravada += resultado_linea['subtotal']

    total_descuento += descuento_global
    total_descuento_con_igv += descuento_global_con_igv
    total_gravada -= descuento_global
    total_igv = suma_igv - (descuento_global_con_igv - descuento_global)
    # total_igv = (total_gravada * Decimal(valor_igv)).quantize(Decimal('0.01'))
    total = (total_gravada + total_inafecta + total_exonerada + total_igv + total_otros_cargos).quantize(Decimal('0.01'))

    respuesta['descuento_global_cotizacion'] = (descuento_global_cotizacion * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['descuento_oferta'] = (descuento_oferta * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['descuento_global'] = (descuento_global * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['descuento_global_con_igv'] = (descuento_global_con_igv * tipo_cambio).quantize(Decimal('0.01'))
    if descuento_global_con_igv >= total_otros_cargos:
        respuesta['descuento_cotizacion'] = ((descuento_global_con_igv - total_otros_cargos) * tipo_cambio).quantize(Decimal('0.01'))
        respuesta['otros_cargos_cotizacion'] = (Decimal('0.00') * tipo_cambio).quantize(Decimal('0.01'))
    else:
        respuesta['descuento_cotizacion'] = (descuento_global_con_igv * tipo_cambio).quantize(Decimal('0.01'))
        respuesta['otros_cargos_cotizacion'] = (total_otros_cargos * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['total_descuento'] = (total_descuento * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['descuento_por_items'] = (respuesta['total_descuento'] - respuesta['descuento_global'])
    respuesta['total_descuento_con_igv'] = (total_descuento_con_igv * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['total_anticipo'] = (total_anticipo * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['total_gravada'] = (total_gravada * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['total_inafecta'] = (total_inafecta * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['total_exonerada'] = (total_exonerada * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['total_igv'] = (total_igv * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['total_gratuita'] = (total_gratuita * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['total_otros_cargos'] = (total_otros_cargos * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['total_icbper'] = (total_icbper * tipo_cambio).quantize(Decimal('0.01'))
    respuesta['total'] = (total * tipo_cambio).quantize(Decimal('0.01'))
    return respuesta


def ver_proveedor(documento):
    if hasattr(documento, 'OfertaProveedorDetalle_oferta_proveedor'):
        proveedor = documento.requerimiento_material.proveedor
        interlocutor_proveedor = documento.requerimiento_material.interlocutor_proveedor
    elif hasattr(documento, 'ComprobanteCompraPIDetalle_comprobante_compra'):
        proveedor = documento.orden_compra.proveedor
        interlocutor_proveedor = documento.orden_compra.interlocutor
    elif hasattr(documento, 'ComprobanteCompraCIDetalle_comprobante_compra'):
        proveedor = documento.comprobante_compra_PI.orden_compra.proveedor
        interlocutor_proveedor = documento.comprobante_compra_PI.orden_compra.interlocutor
    return proveedor, interlocutor_proveedor


def obtener_totales(cabecera, sociedad=None, tipo_cambio=Decimal('1')):
    if hasattr(cabecera, 'OfertaProveedorDetalle_oferta_proveedor'):
        detalles = cabecera.OfertaProveedorDetalle_oferta_proveedor.all()
    elif hasattr(cabecera, 'ComprobanteCompraPIDetalle_comprobante_compra'):
        detalles = cabecera.ComprobanteCompraPIDetalle_comprobante_compra.all()
    elif hasattr(cabecera, 'ComprobanteCompraCIDetalle_comprobante_compra'):
        detalles = cabecera.ComprobanteCompraCIDetalle_comprobante_compra.all()
    elif hasattr(cabecera, 'OrdenCompraDetalle_orden_compra'):
        detalles = cabecera.OrdenCompraDetalle_orden_compra.all()
    elif hasattr(cabecera, 'ComprobanteCompraActivoDetalle_comprobante_compra_activo'):
        detalles = cabecera.ComprobanteCompraActivoDetalle_comprobante_compra_activo.all()
    elif hasattr(cabecera, 'CotizacionVentaDetalle_cotizacion_venta'):
        detalles = cabecera.CotizacionVentaDetalle_cotizacion_venta.all()
    elif hasattr(cabecera, 'ConfirmacionVentaDetalle_confirmacion_venta'):
        detalles = cabecera.ConfirmacionVentaDetalle_confirmacion_venta.all()
    elif hasattr(cabecera, 'FacturaVentaDetalle_factura_venta'):
        detalles = cabecera.FacturaVentaDetalle_factura_venta.all()
    elif hasattr(cabecera, 'BoletaVentaDetalle_boleta_venta'):
        detalles = cabecera.BoletaVentaDetalle_boleta_venta.all()
    elif hasattr(cabecera, 'NotaCreditoDetalle_nota_credito'):
        detalles = cabecera.NotaCreditoDetalle_nota_credito.all()
    lista_resultados_linea = []
    valor_igv = 0
    for detalle in detalles:
        tipo_igv = detalle.tipo_igv
        if sociedad and hasattr(detalle, 'CotizacionSociedad_cotizacion_venta_detalle'):
            cantidad = detalle.CotizacionSociedad_cotizacion_venta_detalle.get(sociedad=sociedad).cantidad
        else:
            cantidad = detalle.cantidad
        precio_unitario_con_igv = detalle.precio_unitario_con_igv
        precio_final_con_igv = detalle.precio_final_con_igv
        if detalle.tipo_igv == 1:
            valor_igv = 0.18
        else:
            valor_igv = 0
        if hasattr(detalle, 'anticipo_regularizacion'):
            anticipo_regularizacion = detalle.anticipo_regularizacion
        else:
            anticipo_regularizacion = False
        calculo = calculos_linea(cantidad, precio_unitario_con_igv, precio_final_con_igv, valor_igv, tipo_igv, anticipo_regularizacion)
        lista_resultados_linea.append(calculo)
    if sociedad and hasattr(cabecera, 'CotizacionDescuentoGlobal_cotizacion_venta'):
        print('Confirmación')
        descuento_global_cotizacion = cabecera.CotizacionDescuentoGlobal_cotizacion_venta.get(sociedad=sociedad).descuento_global_cotizacion
        descuento_oferta = cabecera.CotizacionDescuentoGlobal_cotizacion_venta.get(sociedad=sociedad).descuento_oferta
        descuento_global = cabecera.CotizacionDescuentoGlobal_cotizacion_venta.get(sociedad=sociedad).descuento_global
        otros_cargos = cabecera.CotizacionOtrosCargos_cotizacion_venta.get(sociedad=sociedad).otros_cargos
    else:
        try:
            descuento_global_cotizacion = cabecera.descuento_global_cotizacion
            descuento_oferta = cabecera.descuento_oferta
            descuento_global = cabecera.descuento_global
            otros_cargos = cabecera.otros_cargos
        except:
            try:
                descuento_global_cotizacion = Decimal('0.00')
                descuento_oferta = Decimal('0.00')
                descuento_global = cabecera.descuento_global
                otros_cargos = cabecera.otros_cargos
            except:
                try:
                    descuento_global_cotizacion = Decimal('0.00')
                    descuento_oferta = Decimal('0.00')
                    descuento_global = cabecera.descuento_global
                    otros_cargos = cabecera.total_otros_cargos
                except:
                    descuento_global_cotizacion = Decimal('0.00')
                    descuento_oferta = Decimal('0.00')
                    descuento_global = Decimal('0.00')
                    otros_cargos = Decimal('0.00')

    return calculos_totales(lista_resultados_linea, descuento_global_cotizacion, descuento_oferta, descuento_global, otros_cargos, valor_igv, tipo_cambio)


def obtener_totales_soles(resultado, tipo_cambio, sociedad=None):
    respuesta = {}
    respuesta['descuento_global_cotizacion'] = resultado['descuento_global_cotizacion'] * tipo_cambio
    respuesta['descuento_oferta'] = resultado['descuento_oferta'] * tipo_cambio
    respuesta['descuento_global'] = resultado['descuento_global'] * tipo_cambio
    respuesta['descuento_por_items'] = (resultado['total_descuento'] - resultado['descuento_global']) * tipo_cambio
    respuesta['total_descuento'] = resultado['total_descuento'] * tipo_cambio
    respuesta['total_anticipo'] = resultado['total_anticipo'] * tipo_cambio
    respuesta['total_gravada'] = resultado['total_gravada'] * tipo_cambio
    respuesta['total_inafecta'] = resultado['total_inafecta'] * tipo_cambio
    respuesta['total_exonerada'] = resultado['total_exonerada'] * tipo_cambio
    respuesta['total_igv'] = resultado['total_igv'] * tipo_cambio
    respuesta['total_gratuita'] = resultado['total_gratuita'] * tipo_cambio
    respuesta['total_otros_cargos'] = resultado['total_otros_cargos'] * tipo_cambio
    respuesta['total_icbper'] = resultado['total_icbper'] * tipo_cambio
    respuesta['total'] = resultado['total'] * tipo_cambio
    return respuesta


def numeroXn(numero, n):
    if numero:
        return '0'*(n-len(str(numero))) + str(numero)
    return ""


def igv(fecha=date.today()):
    igv = applications.datos_globales.models.ImpuestoGeneralVentas.objects.filter(fecha_inicio__lte=fecha)
    ipm = applications.datos_globales.models.ImpuestoPromocionMunicipal.objects.filter(fecha_inicio__lte=fecha)
    return igv[0].monto + ipm[0].monto


def tipo_de_cambio(cambio1=None, cambio2=None):
    if cambio1 and cambio2:
        return max(cambio1, cambio2)
    elif cambio1:
        return cambio1
    elif cambio2:
        return cambio2
    else:
        try:
            return applications.datos_globales.models.TipoCambio.objects.tipo_cambio_venta(date.today())
        except:
            return 1


def mes_en_letras(valor):
    meses = {
        1:'ENERO',
        2:'FEBRERO',
        3:'MARZO',
        4:'ABRIL',
        5:'MAYO',
        6:'JUNIO',
        7:'JULIO',
        8:'AGOSTO',
        9:'SETIEMBRE',
        10:'OCTUBRE',
        11:'NOVIEMBRE',
        12:'DICIEMBRE',
    }
    if valor in meses:
        return meses[valor]
    return valor


def fecha_en_letras(fecha):
    try:
        dia = fecha.day
        mes = mes_en_letras(fecha.month).capitalize()
        año = fecha.year
        return '%i de %s de %i' % (dia, mes, año)
    except:
        return "SIN FECHA"


def numero_espacio(texto):
    if texto:
        return str(texto)
    else:
        return ""


def numero_cero(texto):
    if texto:
        return str(texto)
    else:
        return "0.00"


def numero_guion(texto):
    if texto:
        return str(texto)
    else:
        return "-"


def registrar_excepcion(self, ex, fname):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    mensaje = f"{fname} # {exc_tb.tb_lineno} {exc_type} {ex}"
    Excepcion.objects.create(
        texto=mensaje,
        created_by=self.request.user,
        updated_by=self.request.user,
    )
    messages.error(self.request, mensaje)


def obtener_atributos(objeto):
    diccionario = {}
    for att in dir(objeto):
        if att[0] != '_':
            try:
                diccionario[str(att)] = str(getattr(objeto, att))
            except:
                pass
    return json.dumps(diccionario)
    

def get_datetime(date_time):
    fecha, hora = date_time.split('T')
    fecha_split = fecha.split('-')
    hora_split = hora.split(':')
    return datetime(int(fecha_split[0]), int(fecha_split[1]), int(fecha_split[2]), int(hora_split[0]), int(hora_split[1]))