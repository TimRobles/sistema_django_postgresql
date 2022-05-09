import requests
from requests.adapters import HTTPAdapter
from django.core.exceptions import ValidationError
from requests.packages.urllib3.util.retry import Retry

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

def validar_texto(texto):
    lista = texto.split(" ")
    for palabra in lista:
        if not palabra.isalpha():
            raise ValidationError('%s tiene caracteres incorrectos' % texto)

def validar_numero(texto):
    for letra in texto:
        if not letra.isnumeric():
            raise ValidationError('%s tiene caracteres incorrectos' % texto)