from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from datetime import date, datetime
from applications.cobranza.models import Nota
from applications.comprobante_venta.models import FacturaVenta
from applications.cotizacion.models import PrecioListaMaterial
from applications.funciones import registrar_excepcion_sin_user
from applications.home.templatetags.funciones_propias import redondear
from applications.material.funciones import malogrado, stock
from applications.material.models import Material
from applications.pdf import *
from applications.reportes.funciones import DICT_CONTENT_TYPE, DICT_SOCIEDAD, FECHA_HOY, StrToDate, formatoFechaTexto
from applications import reportes
from applications.sociedad.models import Sociedad
from applications.variables import EMAIL_REMITENTE
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.core.files.base import ContentFile

def dataDeudas(TablaEncabezado, TablaDatos, fuenteBase, color):
    encabezado = []
    for encab in TablaEncabezado:
        encabezado.append(parrafoCentro(encab, fuenteBase, 8, 'Bold'))
    
    data = []
    data.append(encabezado)
    
    for dato in TablaDatos:
        fila = []
        fila.append(parrafoCentro(dato[0], fuenteBase, 7))
        fila.append(parrafoCentro(dato[1], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[2], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[3], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[4], fuenteBase, 7))
        fila.append(parrafoCentro(dato[5], fuenteBase, 7))
        fila.append(parrafoCentro(dato[6], fuenteBase, 7))
        fila.append(parrafoCentro(dato[7], fuenteBase, 7))
        fila.append(parrafoCentro(dato[8], fuenteBase, 7))
        fila.append(parrafoIzquierda(dato[9], fuenteBase, 6))
        fila.append(parrafoIzquierda(dato[10], fuenteBase, 7))

        data.append(fila)  

    t=Table(data, repeatRows=1, style=[('GRID',(0,0),(-1,-2),0.5,colors.black),
                        ('GRID',(-8,-2),(-7,-1),0.5,colors.black),
                        ('BOX',(0,0),(-1,-2),1,colors.black),
                        ('BOX',(0,0),(-1,0),1,colors.black),
                        ('BOX',(-8,-1),(-7,-1),1,colors.black), #Inicio(x,y), Fin(x+1,y+1),grosor,color
                        ('BACKGROUND',(-7, 0),(-7,-1),colors.HexColor("#CDCDCD")),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(color)),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('ALIGN',(0,0),(-1,-1),'CENTER')])
    t._argW[0]=cmToPx(1.8)
    t._argW[1]=cmToPx(1.95)
    t._argW[2]=cmToPx(2)
    t._argW[3]=cmToPx(2.1)
    t._argW[4]=cmToPx(2)
    t._argW[5]=cmToPx(2.1)
    t._argW[6]=cmToPx(1.8)
    t._argW[7]=cmToPx(1.5)
    t._argW[8]=cmToPx(1.3)
    t._argW[9]=cmToPx(4)

    return t

def dataCuentas(list_cuenta_dolares, list_cuenta_soles, fuenteBase, color):
    tablaMacro=[]
    filaMacro=[]
    tablaGeneral=[]
    fila=[]
    fila.append(parrafoCentro('Cuentas en DÓLARES: ', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro('Cuentas en SOLES: ', fuenteBase, 10, 'Bold'))
    # fila.append(vacio(1))
    tablaGeneral.append(fila)

    fila=[]

    data=[]
    dato=[]
    dato.append(parrafoCentro('BANCO', fuenteBase, 8, 'Bold'))
    dato.append(parrafoCentro('NÚMERO DE CUENTA', fuenteBase, 8, 'Bold'))
    dato.append(parrafoCentro('CCI', fuenteBase, 8, 'Bold'))
    data.append(dato)

    for lista in list_cuenta_dolares:
        dato=[]
        for item in lista:
            dato.append(parrafoCentro(item, fuenteBase, 8))
        data.append(dato)

    t=Table(data, repeatRows=1, style=[('GRID',(0,0),(-1,-1),1,colors.black),
                        ('BOX',(0,0),(-1,0),2,colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(color)),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('ALIGN',(0,0),(-1,-1),'CENTER')])
    t._argW[0]=cmToPx(2)
    t._argW[1]=cmToPx(5.2)
    t._argW[2]=cmToPx(5.2)
    t.hAlign = 'LEFT'
    fila.append(t)

    data=[]
    dato=[]
    dato.append(parrafoCentro('BANCO', fuenteBase, 8, 'Bold'))
    dato.append(parrafoCentro('NÚMERO DE CUENTA', fuenteBase, 8, 'Bold'))
    dato.append(parrafoCentro('CCI', fuenteBase, 8, 'Bold'))
    data.append(dato)

    for lista in list_cuenta_soles:
        dato=[]
        for item in lista:
            dato.append(parrafoCentro(item, fuenteBase, 8))
        data.append(dato)


    t=Table(data, repeatRows=1, style=[('GRID',(0,0),(-1,-1),1,colors.black),
                        ('BOX',(0,0),(-1,0),2,colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(color)),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('ALIGN',(0,0),(-1,-1),'CENTER')])
    t._argW[0]=cmToPx(2)
    t._argW[1]=cmToPx(5.2)
    t._argW[2]=cmToPx(5.2)
    t.hAlign = 'LEFT'
    fila.append(t)

    tablaGeneral.append(fila)
    t=Table(tablaGeneral)

    filaMacro.append(t)
    tablaMacro.append(filaMacro)
    t=Table(tablaMacro)

    return t

def dataCobranza(TablaEncabezado, TablaDatos, fuenteBase, color):
    encabezado = []
    for encab in TablaEncabezado:
        encabezado.append(parrafoCentro(encab, fuenteBase, 8, 'Bold'))
    
    data = []
    data.append(encabezado)
    
    for dato in TablaDatos:
        fila = []
        fila.append(parrafoIzquierda(dato[0], fuenteBase, 7))
        fila.append(parrafoCentro(dato[1], fuenteBase, 7))
        fila.append(parrafoCentro(dato[2], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[3], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[4], fuenteBase, 7))
        fila.append(parrafoCentro(dato[5], fuenteBase, 7))
        fila.append(parrafoCentro(dato[6], fuenteBase, 7))
        fila.append(parrafoIzquierda(dato[7], fuenteBase, 7))

        data.append(fila)  

    t=Table(data, repeatRows=1, style=[('GRID',(0,0),(-1,-1),0.5,colors.black),
                        ('BOX',(0,0),(-1,-1),1,colors.black),
                        ('BOX',(0,0),(-1,0),1,colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(color)),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('ALIGN',(0,0),(-1,-1),'CENTER')])
    t._argW[0]=cmToPx(9.72)
    t._argW[1]=cmToPx(2.5)
    t._argW[2]=cmToPx(2.5)
    t._argW[3]=cmToPx(2.5)
    t._argW[4]=cmToPx(2.5)
    t._argW[5]=cmToPx(2.5)
    t._argW[6]=cmToPx(2.5)
    # t._argW[7]=cmToPx(2.5)

    return t

def dataResumenStockProductos(TablaEncabezado, TablaDatos, fuenteBase, color):
    encabezado = []
    for encab in TablaEncabezado:
        encabezado.append(parrafoCentro(encab, fuenteBase, 8, 'Bold'))
    
    data = []
    data.append(encabezado)
    
    for dato in TablaDatos:
        fila = []
        fila.append(parrafoCentro(dato[0], fuenteBase, 7))
        fila.append(parrafoIzquierda(dato[1], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[2], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[3], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[4], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[5], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[6], fuenteBase, 7))
        data.append(fila)  

    t=Table(data, repeatRows=1, style=[('GRID',(0,0),(-1,-1),0.5,colors.black),
                        ('BOX',(0,0),(-1,-1),1,colors.black),
                        ('BOX',(0,0),(-1,0),1,colors.black),
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor(color)),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('ALIGN',(0,0),(-1,-1),'CENTER')])
    t._argW[0]=cmToPx(2)
    t._argW[1]=cmToPx(11.5)
    t._argW[2]=cmToPx(2.7)
    t._argW[3]=cmToPx(2.7)
    t._argW[4]=cmToPx(2.7)
    t._argW[5]=cmToPx(2.7)
    # t._argW[6]=cmToPx(2.7)

    return t

def generarReporteDeudas(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color, list_cuenta_dolares, list_cuenta_soles):
    fuenteBase = "ComicNeue"

    data_tabla = dataDeudas(TablaEncabezado, TablaDatos, fuenteBase, color)
    data_tabla_cuentas = dataCuentas(list_cuenta_dolares, list_cuenta_soles, fuenteBase, color)
    elementos = []
    elementos.append(vacio(1))
    elementos.append(Texto[0])
    elementos.append(vacio(1))
    elementos.append(parrafoIzquierda(Texto[1], fuenteBase, 10))
    elementos.append(Texto[2])
    elementos.append(Texto[3])
    elementos.append(vacio(1))
    elementos.append(data_tabla)
    elementos.append(vacio(1.5))
    elementos.append(Texto[4])
    elementos.append(vacio(1.5))
    elementos.append(data_tabla_cuentas)
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf

def generarReporteCobranza(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color):
    fuenteBase = "ComicNeue"

    data_tabla = dataCobranza(TablaEncabezado, TablaDatos, fuenteBase, color)
    elementos = []
    elementos.append(vacio(1.0))
    elementos.append(Texto[0])
    elementos.append(vacio(1.0))
    elementos.append(parrafoIzquierda(Texto[1], fuenteBase, 10))
    elementos.append(vacio(1.0))
    elementos.append(data_tabla)
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf

def generarReporteResumenStockProductos(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color):
    fuenteBase = "ComicNeue"

    data_tabla = dataResumenStockProductos(TablaEncabezado, TablaDatos, fuenteBase, color)
    elementos = []
    # elementos.append(parrafoIzquierda(Texto[0], fuenteBase, 10))
    elementos.append(vacio(2.0))
    elementos.append(data_tabla)
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf


def generar_reporte_cobranza(global_sociedad, titulo):
    sql_cobranza_nota = ''' (SELECT
        MAX(cn.id) AS id,
        CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) AS nro_comprobante,
        SUM(cn.monto) as monto_nota_credito, 
        MAX(cc.razon_social) AS cliente_denominacion,
        'FACTURA' AS tipo_comprobante
        FROM cobranza_nota cn
        LEFT JOIN cobranza_pago cp
            ON cp.id_registro=cn.id AND cp.content_type_id='%s'
        LEFT JOIN cobranza_deuda cd
            ON cp.deuda_id=cd.id  AND cd.content_type_id='%s'
        LEFT JOIN comprobante_venta_facturaventa cvf
            ON cd.id_registro=cvf.id
        LEFT JOIN datos_globales_seriescomprobante dgsc
            ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
        LEFT JOIN clientes_cliente cc
            ON cc.id=cvf.cliente_id
        LEFT JOIN datos_globales_moneda dgm
            ON dgm.id=cn.moneda_id
        WHERE cvf.sociedad_id='%s'
        GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura
        ORDER BY 4)
        UNION
        (SELECT
        MAX(cn.id) AS id,
        CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT),6,'0')) AS nro_comprobante,
        SUM(cn.monto) as monto_nota_credito,
        MAX(cc.razon_social) AS cliente_denominacion,
        'BOLETA' AS tipo_comprobante
        FROM cobranza_nota cn
        LEFT JOIN cobranza_pago cp
            ON cp.id_registro=cn.id AND cp.content_type_id='%s'
        LEFT JOIN cobranza_deuda cd
            ON cp.deuda_id=cd.id  AND cd.content_type_id='%s'
        LEFT JOIN comprobante_venta_boletaventa cvb
            ON cd.id_registro=cvb.id
        LEFT JOIN datos_globales_seriescomprobante dgsc
            ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
        LEFT JOIN clientes_cliente cc
            ON cc.id=cvb.cliente_id
        LEFT JOIN datos_globales_moneda dgm
            ON dgm.id=cn.moneda_id
        WHERE cvb.sociedad_id='%s'
        GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta
        ORDER BY 4) ; ''' %(DICT_CONTENT_TYPE['cobranza | nota'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], global_sociedad, DICT_CONTENT_TYPE['cobranza | nota'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], global_sociedad)
    query_info = Nota.objects.raw(sql_cobranza_nota)

    info_cobranza_nota = []
    for fila in query_info:
        lista_datos = []
        lista_datos.append(fila.nro_comprobante)
        lista_datos.append(fila.monto_nota_credito)
        lista_datos.append(fila.cliente_denominacion)
        lista_datos.append(fila.tipo_comprobante)
        info_cobranza_nota.append(lista_datos)

    dict_cobranza_nota = {}
    for fila in info_cobranza_nota:
        dict_cobranza_nota[fila[0]+'|'+fila[3]] = fila[1]

    sql = '''(SELECT
        MAX(cvf.id) AS id,
        MAX(cc.razon_social) AS cliente_denominacion,
        to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
        CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) AS nro_comprobante,
        MAX(cvf.total) AS monto_facturado,
        MAX(cvf.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - (CASE WHEN MAX(cr.monto) IS NOT NULL THEN MAX(cr.monto) ELSE 0.00 END) AS monto_pendiente,
        to_char(MAX(cvf.fecha_vencimiento), 'DD/MM/YYYY') AS fecha_vencimiento_comprobante,
        CURRENT_DATE - MAX(cvf.fecha_vencimiento) AS dias_para_vencer,
        (CASE WHEN (CURRENT_DATE - MAX(cvf.fecha_vencimiento))>0 THEN 'VENCIDO' ELSE 'PENDIENTE' END) AS estado_vencimiento,
        'FACTURA' AS tipo_comprobante
        FROM comprobante_venta_facturaventa cvf
        LEFT JOIN datos_globales_seriescomprobante dgsc
            ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
        LEFT JOIN clientes_cliente cc
            ON cc.id=cvf.cliente_id
        LEFT JOIN cobranza_deuda cd
            ON cd.content_type_id='%s' AND cd.id_registro=cvf.id
        LEFT JOIN cobranza_pago cp
            ON cp.deuda_id=cd.id AND cp.content_type_id='%s'
        LEFT JOIN cobranza_ingreso ci
            ON ci.id=cp.id_registro
        LEFT JOIN datos_globales_tipocambiosunat dgtcs
            ON ci.fecha=dgtcs.fecha
        LEFT JOIN datos_globales_cuentabancariasociedad dgcb
            ON dgcb.id=ci.cuenta_bancaria_id
        LEFT JOIN datos_globales_moneda dgm
            ON dgm.id=dgcb.moneda_id
        LEFT JOIN cobranza_redondeo cr
            ON cr.deuda_id=cd.id
        WHERE cvf.sociedad_id='%s' AND cvf.estado='4' AND cd.id IS NOT NULL
        GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura
        HAVING (CASE WHEN MAX(cvf.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - (CASE WHEN MAX(cr.monto) IS NOT NULL THEN MAX(cr.monto) ELSE 0.00 END) <= 0.00
            THEN (
                'CANCELADO'
            ) ELSE (
                'PENDIENTE'
            ) END) = 'PENDIENTE'
        ORDER BY cliente_denominacion ASC, fecha_emision_comprobante ASC)
        UNION
        SELECT
        MAX(cvb.id) AS id,
        MAX(cc.razon_social) AS cliente_denominacion,
        to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
        CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT),6,'0')) AS nro_comprobante,
        MAX(cvb.total) AS monto_facturado,
        MAX(cvb.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - (CASE WHEN MAX(cr.monto) IS NOT NULL THEN MAX(cr.monto) ELSE 0.00 END) AS monto_pendiente,
        to_char(MAX(cvb.fecha_vencimiento), 'DD/MM/YYYY') AS fecha_vencimiento_comprobante,
        CURRENT_DATE - MAX(cvb.fecha_vencimiento) AS dias_para_vencer,
        (CASE WHEN (CURRENT_DATE - MAX(cvb.fecha_vencimiento))>0 THEN 'VENCIDO' ELSE 'PENDIENTE' END) AS estado_vencimiento,
        'BOLETA' AS tipo_comprobante
        FROM comprobante_venta_boletaventa cvb
        LEFT JOIN datos_globales_seriescomprobante dgsc
            ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
        LEFT JOIN clientes_cliente cc
            ON cc.id=cvb.cliente_id
        LEFT JOIN cobranza_deuda cd
            ON cd.content_type_id='%s' AND cd.id_registro=cvb.id
        LEFT JOIN cobranza_pago cp
            ON cp.deuda_id=cd.id AND cp.content_type_id='%s'
        LEFT JOIN cobranza_ingreso ci
            ON ci.id=cp.id_registro
        LEFT JOIN datos_globales_tipocambiosunat dgtcs
            ON ci.fecha=dgtcs.fecha
        LEFT JOIN datos_globales_cuentabancariasociedad dgcb
            ON dgcb.id=ci.cuenta_bancaria_id
        LEFT JOIN datos_globales_moneda dgm
            ON dgm.id=dgcb.moneda_id
        LEFT JOIN cobranza_redondeo cr
            ON cr.deuda_id=cd.id
        WHERE cvb.sociedad_id='%s' AND cvb.estado='4' AND cd.id IS NOT NULL
        GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta
        HAVING (CASE WHEN MAX(cvb.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - (CASE WHEN MAX(cr.monto) IS NOT NULL THEN MAX(cr.monto) ELSE 0.00 END) <= 0.00
            THEN (
                'CANCELADO'
            ) ELSE (
                'PENDIENTE'
            ) END) = 'PENDIENTE'
        ORDER BY cliente_denominacion ASC, fecha_emision_comprobante ASC ;''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['cobranza | ingreso'], global_sociedad, DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['cobranza | ingreso'], global_sociedad)
    query_info = FacturaVenta.objects.raw(sql)

    list_cobranza = []
    for fila in query_info:
        lista_datos = []
        lista_datos.append(fila.cliente_denominacion)
        lista_datos.append(fila.fecha_emision_comprobante)
        lista_datos.append(fila.nro_comprobante)
        lista_datos.append(fila.monto_facturado)
        lista_datos.append(fila.monto_pendiente)
        lista_datos.append(fila.fecha_vencimiento_comprobante)
        lista_datos.append(fila.dias_para_vencer)
        lista_datos.append(fila.estado_vencimiento)
        lista_datos.append(fila.tipo_comprobante)
        list_cobranza.append(lista_datos)

    for fila in list_cobranza:
        fila[3] = float(fila[3])
        if fila[4] == None:
            fila[4] = fila[3]
        fila[3] = float(fila[3])
        fila[4] = float(fila[4])

        if fila[2] + '|' + fila[8] in dict_cobranza_nota:
            monto_nota_credito = float(dict_cobranza_nota[fila[2] + '|' + fila[8]])
            fila[4] = fila[4] - monto_nota_credito
        
    objeto_sociedad = Sociedad.objects.get(id=global_sociedad)

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    fecha_texto = formatoFechaTexto(StrToDate(fecha_hoy))

    color = DICT_SOCIEDAD[global_sociedad].color
    #####
    vertical = False
    alinear = 'right'
    logo = [[objeto_sociedad.logo.url, alinear]]
    pie_pagina = objeto_sociedad.pie_pagina
    list_texto = []
    texto = Paragraph('''<para align=center><strong>%s</strong></para>''' %("REPORTE DE COBRANZA"), styleSheet["ComicNeue-Bold-14"])
    list_texto.append(texto)
    texto = '''Lima, %s''' % str(fecha_texto) + '\n''\n' + '''Facturas por cobrar en la semana: '''
    list_texto.append(texto)
    TablaEncabezado = [
        'RAZÓN SOCIAL',
        'FECHA',
        'COMPROB.',
        'TOTAL',
        'PENDIENTE',
        'VENCE',
        'DIAS VENC.',
        'ESTADO',
        ]

    TablaDatos = []
    for lista in list_cobranza:
        if lista[4] > float(0):
            fila = []
            fila.append(lista[0])
            fila.append(lista[1])
            fila.append(lista[2])
            fila.append(lista[3])
            fila.append(lista[4])
            fila.append(lista[5])
            fila.append(lista[6])
            fila.append(lista[7])
            TablaDatos.append(fila)


    buf = generarReporteCobranza(titulo, vertical, logo, pie_pagina, list_texto, TablaEncabezado, TablaDatos, color)

    return buf

def reporte_cobranza():
    try:
        print('reporte_cobranza')
        nombre_archivo_1 = "Reporte_Cobranza_MC_" + str(date.today()) + '.pdf'
        nombre_archivo_2 = "Reporte_Cobranza_MP_" + str(date.today()) + '.pdf'
        archivo_1 = generar_reporte_cobranza(global_sociedad = '1', titulo=nombre_archivo_1)
        archivo_2 = generar_reporte_cobranza(global_sociedad = '2', titulo=nombre_archivo_2)
        asunto = "Recordatorio - Facturas por cobrar " + str(date.today())
        mensaje = "Facturas pendientes por cobrar"
        email_remitente = EMAIL_REMITENTE
        email_destinatario = ["rpaniura@multiplay.com.pe",]
        email_copia = ["trobles@multiplay.com.pe","dprincipal@multiplay.com.pe",]

        correo = EmailMultiAlternatives(subject=asunto, body=mensaje, from_email=email_remitente, to = email_destinatario, cc = email_copia,)
        correo.attach(nombre_archivo_1, archivo_1.getvalue(), 'application/pdf')
        correo.attach(nombre_archivo_2, archivo_2.getvalue(), 'application/pdf')
        correo.attach_alternative(mensaje, "text/html")
        try:
            correo.send()
        except Exception as ex:
            print(ex)
            registrar_excepcion_sin_user(ex, __file__)
    except Exception as ex:
        print("No se pudo enviar el correo..")
        registrar_excepcion_sin_user(ex, __file__)
        print(ex)


#############################################################

def dataReporteStockSociedad(sociedad, fuenteBase, color):
    encabezado = []
    encabezado.append(parrafoCentro('PRODUCTO', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('UNIDAD', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('CANTIDAD', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('PRECIO DE COMPRA', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('TOTAL', fuenteBase, 8, 'Bold'))
    
    total_total = Decimal('0.00')

    data = []
    data.append(encabezado)
    
    for material in Material.objects.all():
        content_type = ContentType.objects.get_for_model(material)
        id_registro = material.id
        id_sociedad = sociedad.id
        precio_lista = PrecioListaMaterial.objects.filter(content_type_producto=content_type, id_registro_producto=id_registro)
        if not precio_lista:
            continue
        stock_material = stock(content_type, id_registro, id_sociedad, id_almacen=None)
        if stock_material <= 0:
            continue
        precio_lista = precio_lista.latest('created_at')
        precio_compra = precio_lista.precio_compra
        simbolo = precio_lista.moneda.simbolo
        total = precio_compra * stock_material
        total_total += total
        
        fila = []
        fila.append(parrafoIzquierda(material.descripcion_venta, fuenteBase))
        fila.append(parrafoIzquierda(material.unidad_base, fuenteBase))
        fila.append(parrafoDerecha(intcomma(redondear(stock_material)), fuenteBase))
        fila.append(parrafoDerecha("%s %s" % (simbolo, intcomma(redondear(precio_compra))), fuenteBase))
        fila.append(parrafoDerecha("%s %s" % (simbolo, intcomma(redondear(total))), fuenteBase))
        data.append(fila)

    fila = []
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(parrafoDerecha("%s %s" % (simbolo, intcomma(redondear(total_total))), fuenteBase))
    data.append(fila)

    t_items=Table(
        data,
        style=[
            ('GRID',(0,0),(-1,-2),1,colors.black),
            ('BOX',(0,0),(-1,-2),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t_items._argW[1]=cmToPx(2.5)
    t_items._argW[2]=cmToPx(2.5)
    t_items._argW[3]=cmToPx(3)
    t_items._argW[4]=cmToPx(3)

    return t_items


def generarReporteStockSociedad(titulo, vertical, logo, pie_pagina, sociedad, color):
    fuenteBase = "ComicNeue"

    data_stock = dataReporteStockSociedad(sociedad, fuenteBase, color)

    elementos = []
    elementos.append(data_stock)
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf

#############################################################

def dataReporteStockMalogradoSociedad(sociedad, fuenteBase, color):
    encabezado = []
    encabezado.append(parrafoCentro('PRODUCTO', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('UNIDAD', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('CANTIDAD', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('PRECIO DE COMPRA', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('TOTAL', fuenteBase, 8, 'Bold'))
    
    total_total = Decimal('0.00')

    data = []
    data.append(encabezado)
    
    for material in Material.objects.all():
        content_type = ContentType.objects.get_for_model(material)
        id_registro = material.id
        id_sociedad = sociedad.id
        precio_lista = PrecioListaMaterial.objects.filter(content_type_producto=content_type, id_registro_producto=id_registro)
        if not precio_lista:
            continue
        stock_material = malogrado(content_type, id_registro, id_sociedad, id_almacen=None)
        if stock_material <= 0:
            continue
        precio_lista = precio_lista.latest('created_at')
        precio_compra = precio_lista.precio_compra
        simbolo = precio_lista.moneda.simbolo
        total = precio_compra * stock_material
        total_total += total
        
        fila = []
        fila.append(parrafoIzquierda(material.descripcion_venta, fuenteBase))
        fila.append(parrafoIzquierda(material.unidad_base, fuenteBase))
        fila.append(parrafoDerecha(intcomma(redondear(stock_material)), fuenteBase))
        fila.append(parrafoDerecha("%s %s" % (simbolo, intcomma(redondear(precio_compra))), fuenteBase))
        fila.append(parrafoDerecha("%s %s" % (simbolo, intcomma(redondear(total))), fuenteBase))
        data.append(fila)

    fila = []
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(parrafoDerecha("%s %s" % (simbolo, intcomma(redondear(total_total))), fuenteBase))
    data.append(fila)

    t_items=Table(
        data,
        style=[
            ('GRID',(0,0),(-1,-2),1,colors.black),
            ('BOX',(0,0),(-1,-2),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t_items._argW[1]=cmToPx(2.5)
    t_items._argW[2]=cmToPx(2.5)
    t_items._argW[3]=cmToPx(3)
    t_items._argW[4]=cmToPx(3)

    return t_items


def generarReporteStockMalogradoSociedad(titulo, vertical, logo, pie_pagina, sociedad, color):
    fuenteBase = "ComicNeue"

    data_stock = dataReporteStockMalogradoSociedad(sociedad, fuenteBase, color)

    elementos = []
    elementos.append(data_stock)
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf