import requests
from requests.adapters import HTTPAdapter
from django.core.exceptions import ValidationError
from requests.packages.urllib3.util.retry import Retry
import applications
import math

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
    