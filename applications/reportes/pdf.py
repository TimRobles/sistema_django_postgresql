from decimal import Decimal
import json
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from datetime import date, datetime, timedelta
from applications.clientes.models import Cliente, ClienteInterlocutor, CorreoCliente, CorreoInterlocutorCliente
from applications.cobranza.models import EnvioDeuda, Nota
from applications.comprobante_venta.models import BoletaVenta, FacturaVenta
from applications.cotizacion.models import PrecioListaMaterial
from applications.datos_globales.models import CuentaBancariaSociedad, Departamento, Moneda
from applications.funciones import registrar_excepcion_sin_user
from applications.home.templatetags.funciones_propias import redondear
from applications.material.funciones import malogrado, stock
from applications.material.models import Material
from applications.nota.models import NotaCredito
from applications.pdf import *
from applications.reportes.funciones import DICT_CONTENT_TYPE, DICT_SOCIEDAD, FECHA_HOY, StrToDate, formatoFechaTexto
from applications import reportes
from applications.sociedad.models import Sociedad
from applications.variables import EMAIL_REMITENTE
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.core.files.base import ContentFile
from django.db.models import Q, F

############################################################# ReporteResumenStockProductos ############################################################# 

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

def generarReporteResumenStockProductos(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color):
    fuenteBase = "ComicNeue"

    data_tabla = dataResumenStockProductos(TablaEncabezado, TablaDatos, fuenteBase, color)
    elementos = []
    # elementos.append(parrafoIzquierda(Texto[0], fuenteBase, 10))
    elementos.append(vacio(2.0))
    elementos.append(data_tabla)
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf

############################################################# ReporteDeudas ############################################################# 

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

def generar_reporte_deudas(global_sociedad, global_cliente, titulo):
    DICT_CLIENTE = {}
    query_cliente = Cliente.objects.all()
    for dato in query_cliente:
        c_id = str(dato.id)
        DICT_CLIENTE[c_id] = dato.razon_social
    sql_productos = ''' (SELECT
        MAX(cvf.id) AS id,
        to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
        CONCAT(MAX(dgs.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT), 6, '0')) AS numero_comprobante,
        STRING_AGG(mm.descripcion_corta, ' | ') AS texto_materiales
        FROM comprobante_venta_facturaventa cvf
        LEFT JOIN datos_globales_seriescomprobante dgs
            ON dgs.id = cvf.serie_comprobante_id AND dgs.tipo_comprobante_id='%s'
        LEFT JOIN comprobante_venta_facturaventadetalle cvfd
            ON cvfd.factura_venta_id=cvf.id
        LEFT JOIN material_material mm
            ON cvfd.content_type_id='%s' AND mm.id=cvfd.id_registro
        WHERE cvf.estado='4'
        GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura)
        UNION
        (SELECT
        MAX(cvb.id) AS id,
        to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
        CONCAT(MAX(dgs.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT), 6, '0')) AS numero_comprobante,
        STRING_AGG(mm.descripcion_corta, ' | ') AS texto_materiales
        FROM comprobante_venta_boletaventa cvb
        LEFT JOIN datos_globales_seriescomprobante dgs
            ON dgs.id = cvb.serie_comprobante_id AND dgs.tipo_comprobante_id='%s'
        LEFT JOIN comprobante_venta_boletaventadetalle cvbd
            ON cvbd.boleta_venta_id=cvb.id
        LEFT JOIN material_material mm
            ON cvbd.content_type_id='%s' AND mm.id=cvbd.id_registro
        WHERE cvb.estado='4'
        GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta)''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['material | material'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['material | material'])
    query_productos = FacturaVenta.objects.raw(sql_productos)
    
    info = []
    for fila in query_productos:
        lista_datos = []
        lista_datos.append(fila.fecha_emision_comprobante)
        lista_datos.append(fila.numero_comprobante)
        lista_datos.append(fila.texto_materiales)
        info.append(lista_datos)

    dict_productos = {}
    for fila in info:
        dict_productos[fila[0]+'|'+fila[1]] = fila[2]

    objeto_sociedad = Sociedad.objects.get(id=global_sociedad)

    # Letras según fechas pactadas al cotizar
    sql_letras = ''' (SELECT
        MAX(cvf.id) AS id, 
        to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
        'FACTURA' AS tipo_comprobante,
        CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) AS nro_comprobante,
        MAX(cc.razon_social) AS cliente_denominacion,
        (CASE WHEN MAX(cvf.tipo_venta)='2'
        THEN (
            STRING_AGG(CONCAT(
                to_char(cobc.fecha, 'DD/MM/YYYY'),
                ' $ ',
                CAST(ROUND(cobc.monto,2) AS TEXT)
                ), '\n' ORDER BY cobc.fecha)
        ) ELSE (
            ''
        ) END) AS letras
        FROM comprobante_venta_facturaventa cvf
        LEFT JOIN datos_globales_seriescomprobante dgsc
            ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
        LEFT JOIN clientes_cliente cc
            ON cc.id=cvf.cliente_id
        LEFT JOIN cobranza_deuda cd
            ON cd.content_type_id='%s' AND cd.id_registro=cvf.id
        LEFT JOIN cobranza_cuota cobc
            ON cobc.deuda_id=cd.id
        WHERE cvf.tipo_venta='2' AND cvf.sociedad_id='%s' AND cd.id IS NOT NULL AND cvf.estado='4'
        GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura
        ORDER BY cliente_denominacion ASC, letras ASC)
        UNION
        (SELECT
        MAX(cvb.id) AS id,
        to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
        'BOLETA' AS tipo_comprobante,
        CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT),6,'0')) AS nro_comprobante,
        MAX(cc.razon_social) AS cliente_denominacion,
        (CASE WHEN MAX(cvb.tipo_venta)='2'
        THEN (
            STRING_AGG(CONCAT(
                to_char(cobc.fecha, 'DD/MM/YYYY'),
                ' $ ',
                CAST(ROUND(cobc.monto,2) AS TEXT)
                ), '\n' ORDER BY cobc.fecha)
        ) ELSE (
            ''
        ) END) AS letras
        FROM comprobante_venta_boletaventa cvb
        LEFT JOIN datos_globales_seriescomprobante dgsc
            ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
        LEFT JOIN clientes_cliente cc
            ON cc.id=cvb.cliente_id
        LEFT JOIN cobranza_deuda cd
            ON cd.content_type_id='%s' AND cd.id_registro=cvb.id
        LEFT JOIN cobranza_cuota cobc
            ON cobc.deuda_id=cd.id
        WHERE cvb.tipo_venta='2' AND cvb.sociedad_id='%s' AND cd.id IS NOT NULL AND cvb.estado='4'
        GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta
        ORDER BY cliente_denominacion ASC, letras ASC)
        ORDER BY cliente_denominacion ASC, letras ASC ;''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], global_sociedad, DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], global_sociedad)                                                               
    query_letras = FacturaVenta.objects.raw(sql_letras)

    info = []
    for fila in query_letras:
        lista_datos = []
        lista_datos.append(fila.fecha_emision_comprobante)
        lista_datos.append(fila.tipo_comprobante)
        lista_datos.append(fila.nro_comprobante)
        lista_datos.append(fila.cliente_denominacion)
        lista_datos.append(fila.letras)
        info.append(lista_datos)

    dict_letras = {}
    for fila in info:
        dict_letras[fila[0]+'|'+fila[1]+'|'+fila[2]] = fila[4]

    # facturas por jarrones -- mejorar esto..
    DICT_FACT_INVALIDAS = {}

    list_fact_invalidas_mpl = [
        'F001-000231',
        'F001-000233',
        'F001-000245',
        'F001-000298',
        ]
    list_fact_invalidas_mca = [
        'F001-002098',
        'F001-002099',
        ]
    DICT_FACT_INVALIDAS['4'] = list_fact_invalidas_mpl
    DICT_FACT_INVALIDAS['3'] = list_fact_invalidas_mca
    DICT_FACT_INVALIDAS['2'] = list_fact_invalidas_mpl
    DICT_FACT_INVALIDAS['1'] = list_fact_invalidas_mca

    sql = ''' (SELECT
        MAX(cn.id) AS id,
        CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) AS nro_comprobante,
        SUM(cp.monto) as monto_nota_credito,
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
        SUM(cp.monto) as monto_nota_credito,
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
        ORDER BY 4) ; ''' % (DICT_CONTENT_TYPE['cobranza | nota'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], global_sociedad, DICT_CONTENT_TYPE['cobranza | nota'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], global_sociedad)
    query_info = Nota.objects.raw(sql)

    info = []
    for fila in query_info:
        lista_datos = []
        lista_datos.append(fila.nro_comprobante)
        lista_datos.append(fila.monto_nota_credito)
        lista_datos.append(fila.cliente_denominacion)
        lista_datos.append(fila.tipo_comprobante)
        info.append(lista_datos)
    
    dict_cobranza_nota = {}
    for fila in info:
        dict_cobranza_nota[fila[0]+'|'+fila[3]] = fila[1]

    sql = ''' (SELECT 
        MAX(cvf.id) AS id,
        to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
        CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) AS nro_comprobante,
        MAX(cc.razon_social) AS cliente_denominacion,
        MAX(cvf.total) AS monto_facturado,
        SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) + SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_amortizado,
        MAX(cvf.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_pendiente,
        (CASE WHEN MAX(cvf.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - (CASE WHEN MAX(cr.monto) IS NOT NULL THEN MAX(cr.monto) ELSE 0.00 END) <= 0.00
            THEN (
                'CANCELADO'
            ) ELSE (
                'PENDIENTE'
            ) END) AS estado_cobranza,
        to_char(MAX(cvf.fecha_vencimiento), 'DD/MM/YYYY') AS fecha_vencimiento_comprobante,
        MAX(cvf.fecha_vencimiento) - MAX(cvf.fecha_emision) AS dias_credito,
        current_date - MAX(cvf.fecha_vencimiento) AS dias_vencimiento,
        '' AS letras,
        '' AS productos,
        'FACTURA' AS tipo_comprobante,
        MAX(cvf.fecha_emision) AS fecha_orden
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
        LEFT JOIN datos_globales_cuentabancariasociedad dgcb
            ON dgcb.id=ci.cuenta_bancaria_id
        LEFT JOIN datos_globales_moneda dgm
            ON dgm.id=dgcb.moneda_id
        LEFT JOIN cobranza_redondeo cr
            ON cr.deuda_id=cd.id
        WHERE cvf.sociedad_id='%s' AND cvf.estado='4' AND cd.id IS NOT NULL AND cc.id = '%s'
        GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura
        HAVING (CASE WHEN MAX(cvf.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - (CASE WHEN MAX(cr.monto) IS NOT NULL THEN MAX(cr.monto) ELSE 0.00 END) <= 0.00
            THEN (
                'CANCELADO'
            ) ELSE (
                'PENDIENTE'
            ) END) = 'PENDIENTE' AND CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) NOT IN %s
        ORDER BY cliente_denominacion ASC, fecha_orden ASC)
        UNION
        (SELECT
        MAX(cvb.id) AS id,
        to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
        CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT),6,'0')) AS nro_comprobante,
        MAX(cc.razon_social) AS cliente_denominacion,
        MAX(cvb.total) AS monto_facturado,
        SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) + SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_amortizado,
        MAX(cvb.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_pendiente,
        (CASE WHEN MAX(cvb.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - (CASE WHEN MAX(cr.monto) IS NOT NULL THEN MAX(cr.monto) ELSE 0.00 END) <= 0.00
            THEN (
                'CANCELADO'
            ) ELSE (
                'PENDIENTE'
            ) END) AS estado_cobranza,
        to_char(MAX(cvb.fecha_vencimiento), 'DD/MM/YYYY') AS fecha_vencimiento_comprobante,
        MAX(cvb.fecha_vencimiento) - MAX(cvb.fecha_emision) AS dias_credito,
        current_date - MAX(cvb.fecha_vencimiento) AS dias_vencimiento,
        '' AS letras,
        '' AS productos,
        'BOLETA' AS tipo_comprobante,
        MAX(cvb.fecha_emision) AS fecha_orden
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
        LEFT JOIN datos_globales_cuentabancariasociedad dgcb
            ON dgcb.id=ci.cuenta_bancaria_id
        LEFT JOIN datos_globales_moneda dgm
            ON dgm.id=dgcb.moneda_id
        LEFT JOIN cobranza_redondeo cr
            ON cr.deuda_id=cd.id
        WHERE cvb.sociedad_id='%s' AND cvb.estado='4' AND cd.id IS NOT NULL AND cc.id = '%s'
        GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta
        HAVING (CASE WHEN MAX(cvb.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - (CASE WHEN MAX(cr.monto) IS NOT NULL THEN MAX(cr.monto) ELSE 0.00 END) <= 0.00
            THEN (
                'CANCELADO'
            ) ELSE (
                'PENDIENTE'
            ) END) = 'PENDIENTE'
        ORDER BY cliente_denominacion ASC, fecha_orden ASC)
        ORDER BY cliente_denominacion ASC, fecha_orden ASC ; ''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['cobranza | ingreso'], global_sociedad, global_cliente, tuple(DICT_FACT_INVALIDAS[global_sociedad]), DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['cobranza | ingreso'], global_sociedad, global_cliente)
    query_info = FacturaVenta.objects.raw(sql)

    list_general = []
    for fila in query_info:
        lista_datos = []
        lista_datos.append(fila.fecha_emision_comprobante)
        lista_datos.append(fila.nro_comprobante)
        lista_datos.append(fila.cliente_denominacion)
        lista_datos.append(fila.monto_facturado)
        lista_datos.append(fila.monto_amortizado)
        lista_datos.append(fila.monto_pendiente)
        lista_datos.append(fila.estado_cobranza)
        lista_datos.append(fila.fecha_vencimiento_comprobante)
        lista_datos.append(fila.dias_credito)
        lista_datos.append(fila.dias_vencimiento)
        lista_datos.append(fila.letras)
        lista_datos.append(fila.productos)
        lista_datos.append(fila.tipo_comprobante)
        list_general.append(lista_datos)

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    for fila in list_general:
        fila[3] = float(fila[3])
        if fila[4] == None:
            fila[4] = '0.00'
        if fila[5] == None:
            fila[5] = fila[3]
        fila[4] = float(fila[4])
        fila[5] = float(fila[5])

        if fila[1] + '|' + fila[12] in dict_cobranza_nota:
            fila[4] += float(dict_cobranza_nota[fila[1] + '|' + fila[12]])
            fila[5] = fila[3] - fila[4]

        # if fila[9] != '':
        #     fecha1 = datetime.strptime(fecha_hoy, '%Y-%m-%d')
        #     fecha2 = datetime.strptime(fila[9], '%Y-%m-%d')
        #     dias = (fecha1 - fecha2) / timedelta(days=1)
        #     fila[9] = str(dias)
        if float(fila[9]) > float(0):
            fila[6] = 'VENCIDO'
        if fila[11] == None:
            fila[11] = ''
        try:
            fila[10] = dict_letras[fila[0]+'|'+fila[12]+'|'+fila[1]]
            div = fila[10].split('\n')
            rest = float(fila[4])
            list_resumen_letra = []
            list_dias = []
            list_estados = []
            for sub_div in div:
                list_fecha_monto = sub_div.split(' $ ')
                fecha_letra = list_fecha_monto[0]
                monto_letra = float(list_fecha_monto[1])
                rest = rest - monto_letra
                if rest >= float(0):
                    estado_letra = "CANCELADO"
                else:
                    fecha_base = datetime.strptime(fecha_hoy, '%Y-%m-%d')
                    fecha_letra_dt = datetime.strptime(fecha_letra, '%d/%m/%Y')
                    dias = (fecha_base - fecha_letra_dt) / timedelta(days=1)
                    if float(dias) > float(0):
                        estado_letra = 'VENCIDO'
                    else:
                        estado_letra = "PENDIENTE"
                        fila_dias = str(dias)[:-2]
                        list_dias.append(fila_dias)

                    fila_estado = estado_letra
                    list_estados.append(fila_estado)

                fila_letra = fecha_letra + ' $ ' + str(monto_letra) + ' ' + estado_letra
                list_resumen_letra.append(fila_letra)
            fila[10] = '\n'.join(list_resumen_letra)
            fila.insert(13,list_dias)
            fila.insert(14,list_estados)
                
        except:
            fila[10] = ''
            fila.insert(13,[])
            fila.insert(14,[])
    
    fecha_texto = formatoFechaTexto(StrToDate(fecha_hoy))
    fecha_invertida = datetime.now().strftime("%d-%m-%Y")

    color = DICT_SOCIEDAD[global_sociedad].color
    #####
    # query_sociedad = Sociedad.objects.filter(id = int(global_sociedad))[0]
    # abreviatura = query_sociedad.abreviatura
    # #####
    # titulo = "Reporte de Deudas - " + abreviatura + " - " + DICT_CLIENTE[global_cliente] + " - " + FECHA_HOY
    vertical = False
    alinear = 'right'
    logo = [[objeto_sociedad.logo.url, alinear]]
    pie_pagina = objeto_sociedad.pie_pagina
    list_texto = []
    # texto = '''Lima, %s''' % str(fecha_texto) + '\n''\n' + '''SR. ''' + DICT_CLIENTE[global_cliente] + '\n' + '''Estimado cliente, se le remite la deuda actualizada al día de hoy <strong>%s</strong>, cuyos detalles son los siguientes:''' % (str(fecha_hoy))
    text = Paragraph('''<para align=center><strong>%s</strong></para>''' %("REPORTE DE DEUDAS"), styleSheet["ComicNeue-Bold-14"])
    list_texto.append(text)
    text = '''Lima, %s''' % str(fecha_texto) + '\n''\n'
    list_texto.append(text)
    text = Paragraph('''<b>SR. ''' + DICT_CLIENTE[global_cliente] + '''</b>''')
    list_texto.append(text)
    text = Paragraph('''Estimado cliente, se le remite la deuda actualizada al día de hoy <strong>%s</strong>, cuyos detalles son los siguientes:''' % (str(fecha_invertida)))
    list_texto.append(text)

    TablaEncabezado = [
        'FECHA',
        'NRO. COMPROBANTE',
        'FACTURADO',
        'AMORTIZADO',
        'PENDIENTE',
        'ESTADO',
        'FEC. VENC.',
        'CRÉDITO',
        'DIAS VENC.',
        'LETRAS',
        'PRODUCTOS',
        ]
    suma_deuda_total = 0

    TablaDatos = []
    for lista in list_general:
        if "VENCIDO" in lista[14]: 
            if lista[5] >= float(100):
                fila = []
                fila.append(lista[0])
                fila.append(lista[1])
                fila.append(lista[3])
                fila.append(lista[4])
                fila.append(lista[5])
                suma_deuda_total += float(lista[5])
                fila.append(lista[6])
                fila.append(lista[7])
                fila.append(lista[8])
                fila.append(lista[9])
                fila.append(lista[10])
                fila.append(dict_productos[lista[0]+'|'+lista[1]])
                TablaDatos.append(fila)
        else:
            if any(float(numero) > float(-8) for numero in lista[13]):
                if lista[5] >= float(100):
                    fila = []
                    fila.append(lista[0])
                    fila.append(lista[1])
                    fila.append(lista[3])
                    fila.append(lista[4])
                    fila.append(lista[5])
                    suma_deuda_total += float(lista[5])
                    fila.append(lista[6])
                    fila.append(lista[7])
                    fila.append(lista[8])
                    fila.append(lista[9])
                    fila.append(lista[10])
                    fila.append(dict_productos[lista[0]+'|'+lista[1]])
                    TablaDatos.append(fila)


    TablaDatos.append(["","","", "Deuda Total:", round(suma_deuda_total,2) ,"","","","","","",""])

    # texto = '''Agradeceremos pueda realizar los pagos a nombre de <strong>%s</strong> y confirmarnos el pago en cualquiera de las siguientes cuentas:''' % DICT_SOCIEDAD[global_sociedad].razon_social
    # list_texto.append(texto)

    text = Paragraph('''Agradeceremos pueda realizar los pagos a nombre de <strong>%s</strong> y confirmarnos el pago en cualquiera de las siguientes cuentas:''' % DICT_SOCIEDAD[global_sociedad].razon_social)
    list_texto.append(text)

    sql_cuentas_bancarias = '''SELECT
        dgcb.id,
        dgb.nombre_comercial AS nombre_banco,
        dgcb.numero_cuenta AS cuenta_banco,
        dgcb.numero_cuenta_interbancaria AS cuenta_cci_banco,
        dgm.nombre AS moneda_descripcion
        FROM datos_globales_cuentabancariasociedad dgcb
        LEFT JOIN datos_globales_banco dgb
            ON dgb.id=dgcb.banco_id
        LEFT JOIN datos_globales_moneda dgm
            ON dgm.id=dgcb.moneda_id
        LEFT JOIN sociedad_sociedad ss
            ON ss.id=dgcb.sociedad_id
        WHERE dgcb.sociedad_id='%s' AND dgcb.estado='1' AND dgcb.efectivo=False''' %(global_sociedad)
    query_info_cuentas = CuentaBancariaSociedad.objects.raw(sql_cuentas_bancarias)

    info_cuentas = []
    for fila in query_info_cuentas:
        lista_datos = []

        lista_datos.append(fila.nombre_banco)
        lista_datos.append(fila.cuenta_banco)
        lista_datos.append(fila.cuenta_cci_banco)
        lista_datos.append(fila.moneda_descripcion)
        info_cuentas.append(lista_datos)


        list_cuenta_dolares, list_cuenta_soles = [], []
        for fila in info_cuentas:
            if 'SOL' in fila[3]: # SOLES
                list_temp = []
                list_temp.extend([fila[0], fila[1], fila[2]])
                list_cuenta_soles.append(list_temp)
            if 'DÓLAR' in fila[3]: # DOLARES
                list_temp = []
                list_temp.extend([fila[0], fila[1], fila[2]])
                list_cuenta_dolares.append(list_temp)

    buf = generarReporteDeudas(titulo, vertical, logo, pie_pagina, list_texto, TablaEncabezado, TablaDatos, color, list_cuenta_dolares, list_cuenta_soles)

    # respuesta = HttpResponse(buf.getvalue(), content_type='application/pdf')
    # respuesta.headers['content-disposition']='inline; filename=%s.pdf' % titulo

    return buf

def reporte_deuda(global_sociedad):
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
        WHERE cvf.sociedad_id='%s' AND cvf.tipo_venta='2'
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
        WHERE cvb.sociedad_id='%s' AND cvb.tipo_venta='2'
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
        WHERE cvf.sociedad_id='%s' AND cvf.tipo_venta='2' AND cvf.estado='4' AND cd.id IS NOT NULL
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
        WHERE cvb.sociedad_id='%s' AND cvb.tipo_venta='2' AND cvb.estado='4' AND cd.id IS NOT NULL
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

    TablaDatos = []
    for lista in list_cobranza:
        if lista[4] >= float(100):
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

    clientes_deudores =  list(set(sublista[0] for sublista in TablaDatos if sublista))
    clientes= Cliente.objects.filter(
        razon_social__in = clientes_deudores,

    ).values_list('id', flat=True)

    clientes=list(clientes)
    print(len(clientes))

    # Crear un diccionario para almacenar los correos por cliente
    clientes_correos = {}
    interlocutores_correos = {}

    # Recorrer cada cliente
    for cliente in clientes:
        # Obtener los correos asociados directamente al cliente
        correos_cliente = CorreoCliente.objects.filter(cliente=cliente).values_list('correo', flat=True)

        interlocutores = ClienteInterlocutor.objects.filter(cliente=cliente).values_list('interlocutor', flat=True) # Obtener los interlocutores del cliente
        correos_interlocutores = CorreoInterlocutorCliente.objects.filter(interlocutor__in=interlocutores).values_list('correo', flat=True) # Obtener los correos de los interlocutores
        # todos_los_correos = list(correos_cliente) + list(correos_interlocutores) # Unir los correos del cliente y de los interlocutores
        
        # Añadir al diccionario con el cliente como clave y los correos como valor
        clientes_correos[cliente] = list(correos_cliente)
        interlocutores_correos[cliente] = list(correos_interlocutores)

    return clientes, clientes_correos,interlocutores_correos

def reporte_cobranza_deudor():
    try:
        print('reporte_cobranza_deudor')

        sociedades = Sociedad.objects.only('id','razon_social').exclude(id=1).order_by('id')
        envio_dict = {}

        for sociedad in sociedades:
            data = reporte_deuda(global_sociedad = str(sociedad.id))
            envio_dict[str(sociedad.id)] = []
            for cliente in data[0]:
                titulo = "Reporte de Deudas - " + FECHA_HOY
                archivo = generar_reporte_deudas(global_sociedad = str(sociedad.id), global_cliente=str(cliente), titulo=titulo)
                asunto = "Recordatorio - Deudas Pendientes " + str(date.today())
                mensaje = "Estimado cliente, usted cuenta con deudas pendientes por cancelar."
                email_remitente = EMAIL_REMITENTE
 
                email_destinatario = data[1].get(cliente)
                if email_destinatario == []:
                    email_destinatario = data[2].get(cliente)
                email_copia = ["rpaniura@multiplay.com.pe","dprincipal@multiplay.com.pe",]

                # email_destinatario = ["rore@multiplay.com.pe",]
                # email_copia = []
                correo = EmailMultiAlternatives(subject=asunto, body=mensaje, from_email=email_remitente, to = email_destinatario, cc = email_copia,)
                correo.attach(titulo, archivo.getvalue(), 'application/pdf')
                correo.attach_alternative(mensaje, "text/html")

                estado_envio = False
                try:
                    correo.send()
                    estado_envio = True
                except Exception as ex:
                    print(ex)
                    registrar_excepcion_sin_user(ex, __file__)
                
                # Guardamos la información de envío para este cliente
                envio_dict[str(sociedad.id)].append([str(cliente), email_destinatario, estado_envio])

        # Guardamos el registro en EnvioDeuda para todas las sociedades
        EnvioDeuda.objects.create(
            envio=json.dumps(envio_dict),
            fecha=timezone.now().date(),
            created_by=None,  # Asumiendo que no hay un usuario actual
            updated_by=None   # Asumiendo que no hay un usuario actual
        )

    except Exception as ex:
        print("No se pudieron enviar los correo..")
        registrar_excepcion_sin_user(ex, __file__)
        print(ex)
        
    envio_deuda = EnvioDeuda.objects.latest('fecha')
    envio_dict = json.loads(envio_deuda.envio)

    for sociedad_id, clientes in envio_dict.items():
        print(f"Sociedad {sociedad_id}:")
        for cliente in clientes:
            print(f"  Cliente {cliente[0]}: Email {cliente[1]}, Enviado: {cliente[2]}")
    
############################################################# ReporteCobranza #############################################################

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
        WHERE cvf.sociedad_id='%s' AND cvf.tipo_venta='2'
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
        WHERE cvb.sociedad_id='%s' AND cvb.tipo_venta='2'
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
        WHERE cvf.sociedad_id='%s' AND cvf.tipo_venta='2' AND cvf.estado='4' AND cd.id IS NOT NULL
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
        WHERE cvb.sociedad_id='%s'  AND cvb.tipo_venta='2' AND cvb.estado='4' AND cd.id IS NOT NULL
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
        if lista[4] > float(100):
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
        nombre_archivo_3 = "Reporte_Cobranza_MF_" + str(date.today()) + '.pdf'
        nombre_archivo_4 = "Reporte_Cobranza_WF_" + str(date.today()) + '.pdf'
        archivo_1 = generar_reporte_cobranza(global_sociedad = '1', titulo=nombre_archivo_1)
        archivo_2 = generar_reporte_cobranza(global_sociedad = '2', titulo=nombre_archivo_2)
        archivo_3 = generar_reporte_cobranza(global_sociedad = '3', titulo=nombre_archivo_3)
        archivo_4 = generar_reporte_cobranza(global_sociedad = '4', titulo=nombre_archivo_4)
        asunto = "Recordatorio - Facturas por cobrar " + str(date.today())
        mensaje = "Facturas pendientes por cobrar"
        email_remitente = EMAIL_REMITENTE
        email_destinatario = ["rpaniura@multiplay.com.pe",]
        email_copia = ["trobles@multiplay.com.pe","dprincipal@multiplay.com.pe",]

        correo = EmailMultiAlternatives(subject=asunto, body=mensaje, from_email=email_remitente, to = email_destinatario, cc = email_copia,)
        correo.attach(nombre_archivo_1, archivo_1.getvalue(), 'application/pdf')
        correo.attach(nombre_archivo_2, archivo_2.getvalue(), 'application/pdf')
        correo.attach(nombre_archivo_3, archivo_3.getvalue(), 'application/pdf')
        correo.attach(nombre_archivo_4, archivo_4.getvalue(), 'application/pdf')
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

############################################################# ReporteStockSociedad #############################################################

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

############################################################# ReporteStockMalogradoSociedad #############################################################

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

############################################################# ReporteVentasDepartamento #############################################################

def dataReporteVentasDepartamento(fecha_inicio, fecha_fin, departamento, fuenteBase, color):
    moneda_base = Moneda.objects.get(simbolo='$')
    
    encabezado = []
    encabezado.append(parrafoCentro('CLIENTE', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('DOCUMENTO', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('DIRECCIÓN', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('TOTAL FACTURAS', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('TOTAL BOLETAS', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('TOTAL NOTAS DE CRÉDITO', fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro('TOTAL', fuenteBase, 8, 'Bold'))
    
    total_total = Decimal('0.00')

    data = []
    
    for cliente in Cliente.objects.filter(distrito__provincia__departamento=departamento):
        total = Decimal('0.00')
        total_factura = Decimal('0.00')
        for factura in FacturaVenta.objects.filter(cliente=cliente, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin):
            if factura.moneda == moneda_base:
                total_factura += factura.total
            else:
                total_factura += (factura.total / factura.tipo_cambio).quantize(Decimal('0.01'))

        total_boleta = Decimal('0.00')
        for boleta in BoletaVenta.objects.filter(cliente=cliente, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin):
            if boleta.moneda == moneda_base:
                total_boleta += boleta.total
            else:
                total_boleta += (boleta.total / boleta.tipo_cambio).quantize(Decimal('0.01'))

        total_nota_credito = Decimal('0.00')
        for nota_credito in NotaCredito.objects.filter(cliente=cliente, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin):
            if nota_credito.moneda == moneda_base:
                total_nota_credito += nota_credito.total
            else:
                total_nota_credito += (nota_credito.total / nota_credito.tipo_cambio).quantize(Decimal('0.01'))

        total = total_factura + total_boleta - total_nota_credito
        total_total += total
        
        fila = []
        fila.append(parrafoIzquierda(cliente.razon_social, fuenteBase))
        fila.append(parrafoIzquierda(f"{cliente.documento} - {cliente.numero_documento}", fuenteBase))
        fila.append(parrafoIzquierda(cliente.direccion_fiscal, fuenteBase))
        fila.append(parrafoDerecha("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_factura))), fuenteBase))
        fila.append(parrafoDerecha("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_boleta))), fuenteBase))
        fila.append(parrafoDerecha("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_nota_credito))), fuenteBase))
        fila.append(parrafoDerecha("%s %s" % (moneda_base.simbolo, intcomma(redondear(total))), fuenteBase))
        fila.append(total)
        data.append(fila)

    data.sort(key = lambda i: i[7], reverse=True) #Total
    for dato in data:
        dato.pop(7)
    
    data.insert(0, encabezado)

    fila = []
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(parrafoDerecha("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_total))), fuenteBase))
    data.append(fila)

    t_items=Table(
        data,
        style=[
            ('GRID',(0,0),(-1,-2),1,colors.black),
            ('BOX',(0,0),(-1,-2),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ],
        repeatRows=1
        )
    t_items._argW[0]=cmToPx(5)
    t_items._argW[1]=cmToPx(3.5)
    t_items._argW[3]=cmToPx(2.5)
    t_items._argW[4]=cmToPx(2.5)
    t_items._argW[5]=cmToPx(2.5)
    t_items._argW[6]=cmToPx(2.5)

    return t_items

def generarReporteVentasDepartamento(titulo, vertical, logo, pie_pagina, fecha_inicio, fecha_fin, departamento_codigo, color):
    fuenteBase = "ComicNeue"
    if departamento_codigo:
        departamentos = Departamento.objects.filter(codigo=departamento_codigo)
    else:
        departamentos = Departamento.objects.all()
    
    elementos = []
    for departamento in departamentos:
        data_ventas = dataReporteVentasDepartamento(fecha_inicio, fecha_fin, departamento, fuenteBase, color)

        elementos.append(parrafoCentro(departamento.nombre, fuenteBase, 12, 'Bold'))
        elementos.append(parrafoCentro(f"{fecha_inicio.strftime('%d/%m/%Y')} - {fecha_fin.strftime('%d/%m/%Y')}", fuenteBase, 12, 'Bold'))
        elementos.append(vacio())
        elementos.append(data_ventas)
        if len(departamentos)>1:
            elementos.append(PageBreak())
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf