import requests
from decimal import Decimal
from requests.adapters import HTTPAdapter
from django.core.exceptions import ValidationError
from requests.packages.urllib3.util.retry import Retry
import applications
import math
import random
import string

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


def calculos_linea(cantidad, precio_unitario_con_igv, precio_final_con_igv, valor_igv):
    respuesta = {}

    precio_unitario_sin_igv = Decimal(Decimal(precio_unitario_con_igv)/(1 + Decimal(valor_igv))).quantize(Decimal('0.0000000001'))

    precio_final_sin_igv = Decimal(Decimal(precio_final_con_igv)/(1 + Decimal(valor_igv))).quantize(Decimal('0.0000000001'))

    descuento_unitario = (precio_unitario_sin_igv - precio_final_sin_igv).quantize(Decimal('0.0000000001'))
    descuento = (descuento_unitario * Decimal(cantidad)).quantize(Decimal('0.01'))

    subtotal = (Decimal(cantidad) * precio_unitario_sin_igv - descuento).quantize(Decimal('0.01'))
    igv = (subtotal * Decimal(valor_igv)).quantize(Decimal('0.01'))
    total = (subtotal + igv).quantize(Decimal('0.01'))

    respuesta['precio_unitario_sin_igv'] = precio_unitario_sin_igv
    respuesta['descuento'] = descuento
    respuesta['subtotal'] = subtotal
    respuesta['igv'] = igv
    respuesta['total'] = total

    return respuesta


def calculos_totales(lista_resultados_linea, descuento_global, otros_cargos, internacional, anticipo, valor_igv):
    respuesta = {}

    suma_igv = Decimal('0.00')
    descuento_global = Decimal('0.00')
    total_descuento = Decimal('0.00')
    total_gravada = Decimal('0.00')
    total_inafecta = Decimal('0.00')
    total_exonerada = Decimal('0.00')
    total_anticipo = Decimal('0.00')

    total_gratuita = Decimal('0.00')
    total_otros_cargos = otros_cargos
    total_isc = Decimal('0.00')
    total = Decimal('0.00')

    for resultado_linea in lista_resultados_linea:
        suma_igv += resultado_linea['igv']

        total_descuento += resultado_linea['descuento']
        if internacional == True:
            total_gravada += resultado_linea['subtotal']
        else:
            total_exonerada += resultado_linea['subtotal']

    total_descuento += descuento_global
    total_igv = (total_gravada * Decimal(valor_igv)).quantize(Decimal('0.01'))
    if anticipo:
        total_anticipo = (total_gravada + total_inafecta + total_exonerada + total_igv + total_otros_cargos).quantize(Decimal('0.01'))
    else:
        total = (total_gravada + total_inafecta + total_exonerada + total_igv + total_otros_cargos).quantize(Decimal('0.01'))

    respuesta['descuento_global'] = descuento_global
    respuesta['total_descuento'] = total_descuento
    respuesta['total_anticipo'] = total_anticipo
    respuesta['total_gravada'] = total_gravada
    respuesta['total_inafecta'] = total_inafecta
    respuesta['total_exonerada'] = total_exonerada
    respuesta['total_igv'] = total_igv
    respuesta['total_gratuita'] = total_gratuita
    respuesta['total_otros_cargos'] = total_otros_cargos
    respuesta['total_isc'] = total_isc
    respuesta['total'] = total
    return respuesta


def obtener_totales(cabecera):
    detalles = cabecera.OfertaProveedorDetalle_oferta_proveedor.all()
    lista_resultados_linea = []
    for detalle in detalles:
        cantidad = detalle.cantidad
        precio_unitario_con_igv = detalle.precio_unitario_con_igv
        precio_final_con_igv = detalle.precio_final_con_igv
        if detalle.tipo_igv == 1:
            valor_igv = 0.18
        else:
            valor_igv = 0
        calculo = calculos_linea(cantidad, precio_unitario_con_igv, precio_final_con_igv, valor_igv)
        lista_resultados_linea.append(calculo)
    descuento_global = cabecera.descuento_global
    otros_cargos = 0
    internacional = cabecera.internacional_nacional
    anticipo = False
    return calculos_totales(lista_resultados_linea, descuento_global, otros_cargos, internacional, anticipo, valor_igv)