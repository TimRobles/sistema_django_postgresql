# Script que consulta el estado de un tramite en la SUNARP y envia una notificación a slack cuando cambia de estado
import requests
import json
from time import sleep
SLACK_REQUIREMENT_CHANNEL_URL = 'https://hooks.slack.com/services/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'

def send_slack(message):
    slack_message = {
        'text': message,
    }
    r = requests.post(SLACK_REQUIREMENT_CHANNEL_URL, json=slack_message)
    return r

def obtener_estado():
    url = "https://tracking-sunarp-production.apps.paas.sunarp.gob.pe/tracking/api/consultaTitulo"

    payload = json.dumps({
    "codigoZona": "01",
    "codigoOficina": "01",
    "anioTitulo": "2024",
    "numeroTitulo": "01711904",
    "ip": "pms.sunarp.gob.pe",
    "userApp": "extranet",
    "userCrea": "11111",
    "status": "A"
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    estado = data['lstTitulo'][0]['estadoActual']
    return estado

def funcion_sunarp():
    # Ejecutar el script cada 15 minutos hasta que el estado cambie
    send_slack(f'Iniciando función')
    contador = 0
    while True:
        estado = obtener_estado()
        if estado != 'EN CALIFICACIÓN':
            send_slack(f'El estado es {estado}')
            contador += 1
            if contador == 3:
                break
        else:
            print('Aun no ha cambiado')
        # Esperar 15 minutos
        sleep(900)
    send_slack(f'Finalizando función')

