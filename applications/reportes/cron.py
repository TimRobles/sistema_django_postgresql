import json
import os
from datetime import datetime
from django.core.mail import EmailMultiAlternatives
from applications.sociedad.models import Sociedad
from applications.variables import EMAIL_REMITENTE
from applications.reportes.pdf import generar_reporte_cobranza, resumen_comercial, resumen_ingresos, resumen_ventas
def funcion_iterativa():
    with open("/webapps/sistema_django_prod/sistema_django_postgresql/applications/reportes/diccionario.json", "r") as infile:
        diccionario = json.load(infile)
        ahora = f"{datetime.now()}"
        diccionario[len(diccionario)+1] = ahora
        with open("/webapps/sistema_django_prod/sistema_django_postgresql/applications/reportes/diccionario.json", "w") as outfile:
            json.dump(diccionario, outfile, indent=4)


def reportes_viernes():
    start = datetime.now()
    print("Generando reportes de viernes...")
    asunto = "Reporte de cobranza de deudores de la semana"
    mensaje = f"Buenos días, se adjuntan los reportes correspondientes al {datetime.now().strftime('%d/%m/%Y')}\n\n- Reporte de cobranza\n- Resumen de Ingresos\n- Resumen de Ventas\n- Resumen de Ventas por comercial\n\nSaludos cordiales."
    email_remitente = EMAIL_REMITENTE
    correos_para = [
        'trobles@multiplay.com.pe',
        'salvarez@multiplay.com.pe',
        'fmaldonado@multiplay.com.pe',
        'rpaniura@multiplay.com.pe',
        'gzuniga@multiplay.com.pe',
    ]
    correo = EmailMultiAlternatives(subject=asunto, body=mensaje, from_email=email_remitente, to=correos_para)

    sociedades = [
        ["1", "MCA"], #Multicable
        ["2", "MPL"], #Multi Play
        ["3", "MFS"], #Multi Fiber
        ["4", "WFS"] #Winning Fiber
        ]
    print("Generando reportes de cobranza...")
    for sociedad in sociedades:
        titulo = f"Reporte de Cobranza - {sociedad[1]} - {datetime.now().strftime('%Y-%m-%d')}"
        archivo = generar_reporte_cobranza(sociedad[0], titulo)
        correo.attach(titulo, archivo.getvalue(), 'application/pdf')
        print(f"Adjuntando reporte de cobranza de {sociedad[1]}...")

    titulo = f"Reporte de Ingresos - {datetime.now().strftime('%Y-%m-%d')}"
    print("Generando resumen de ingresos...")
    archivo = resumen_ingresos()
    correo.attach(titulo, archivo.getvalue(), 'application/pdf')
    print("Adjuntando resumen de ingresos...")

    titulo = f"Reporte de Ventas - {datetime.now().strftime('%Y-%m-%d')}"
    print("Generando resumen de ventas...")
    archivo = resumen_ventas()
    correo.attach(titulo, archivo.getvalue(), 'application/pdf')
    print("Adjuntando resumen de ventas...")

    titulo = f"Reporte por Comercial - {datetime.now().strftime('%Y-%m-%d')}"
    print("Generando resumen por comercial...")
    archivo = resumen_comercial()
    correo.attach(titulo, archivo.getvalue(), 'application/pdf')
    print("Adjuntando resumen por comercial...")
    
    print("Enviando correos...")
    correo.send()
    print("Correos enviados")
    print("Eliminando archivos...")
    archivos = [
        "reporte_ingresos.png",
        "reporte_ventas.png",
        "reporte_comercial.png",
        "reporte_credito.png",
        "reporte_ingresos.xlsx",
        "reporte_ventas.xlsx",
        "reporte_comercial.xlsx",
        "reporte_credito.xlsx",
        ]
    for archivo in archivos:
        try:
            os.remove(archivo)
        except:
            pass
    print("Archivos eliminados")
    print(f"Proceso finalizado en {datetime.now()-start}")