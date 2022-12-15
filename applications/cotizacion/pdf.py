from decimal import Decimal
from applications.datos_globales.models import CuentaBancariaSociedad
from applications.pdf import *

def dataCabeceraCotizacionVenta(Cabecera, fuenteBase):
    data = []
    fila=[]
    fila.append(parrafoIzquierda('Nro. Cotización', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['nro_cotizacion'], fuenteBase, 10))
    fila.append(parrafoDerecha('Lima, ' + Cabecera['fecha_cotizacion'], fuenteBase, 10))
    fila.append('')
    fila.append('')
    data.append(fila)

    fila=[]
    fila.append(parrafoIzquierda('Razón Social', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['razon_social'], fuenteBase, 10))
    fila.append(parrafoIzquierda(Cabecera['tipo_documento'], fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['nro_documento'], fuenteBase, 10))
    data.append(fila)

    fila=[]
    fila.append(parrafoIzquierda('Dirección', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['direccion'], fuenteBase, 10))
    fila.append('')
    fila.append('')
    fila.append('')
    data.append(fila)

    fila=[]
    fila.append(parrafoIzquierda('Contacto', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['interlocutor'], fuenteBase, 10))
    fila.append(parrafoIzquierda('Fecha de Vencimiento', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['fecha_validez'], fuenteBase, 10))
    data.append(fila)

    fila=[]
    fila.append(parrafoIzquierda('Vendedor', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['vendedor'], fuenteBase, 10))
    data.append(fila)

    t=Table(
        data,
        style=[
            # ('GRID',(0,0),(-1,-1),1,colors.black),
            # ('BOX',(0,0),(-1,-1),2,colors.black),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('SPAN',(3,0),(-1,0)),
            ('SPAN',(2,1),(2,1)),
            ('SPAN',(2,2),(-1,2)),
            ('SPAN',(2,3),(2,3)),
            ]
        )
    t._argW[0]=cmToPx(3)
    t._argW[1]=cmToPx(0.5)
    t._argW[3]=cmToPx(3.8)
    t._argW[4]=cmToPx(0.5)
    t._argW[5]=cmToPx(5)

    return t

def dataCotizacionVenta(TablaEncabezado, TablaDatos, TablaTotales, fuenteBase, color, moneda):
    simbolo = moneda.simbolo
    encabezado = []
    for encab in TablaEncabezado:
        encabezado.append(parrafoCentro(encab, fuenteBase, 8, 'Bold'))
    
    data = []
    data.append(encabezado)
    
    for dato in TablaDatos:
        fila = []
        fila.append(parrafoCentro(dato[0], fuenteBase))
        fila.append(parrafoIzquierda(dato[1], fuenteBase))
        fila.append(parrafoIzquierda(dato[2], fuenteBase))
        fila.append(parrafoDerecha(dato[3], fuenteBase))
        fila.append(parrafoDerecha("%s %s" % (simbolo, dato[4]), fuenteBase))
        fila.append(parrafoDerecha("%s %s" % (simbolo, dato[5]), fuenteBase))
        if dato[6] > Decimal('0.00'):
            fila.append(parrafoDerecha("%s -%s" % (simbolo, dato[6]), fuenteBase, color='red'))        
        else:
            fila.append(parrafoDerecha("%s %s" % (simbolo, dato[6]), fuenteBase))        
        fila.append(parrafoDerecha("%s %s" % (simbolo, dato[7]), fuenteBase))        
        fila.append(parrafoDerecha(dato[8], fuenteBase, tamaño=6))        

        data.append(fila)

    t_items=Table(
        data,
        style=[
            ('GRID',(0,0),(-2,-1),1,colors.black),
            ('BOX',(0,0),(-2,-1),2,colors.black),
            ('BACKGROUND', (0, 0), (-2, 0), color),
            ('BACKGROUND', (5, 1), (5, -1), colors.lightgrey),
            # ('GRID',(0,0),(-2,-(totales+1)),1,colors.black),
            # ('GRID',(6,-(totales)),(-3,-1),1,colors.black),
            # ('BOX',(0,0),(-2,-(totales+1)),2,colors.black),
            # ('BOX',(6,-(totales)),(-3,-1),2,colors.black),
            # ('BACKGROUND', (0, 0), (-2, 0), color),
            # ('BACKGROUND', (5, 1), (5, -(totales+1)), colors.lightgrey),
            # ('BACKGROUND', (6,-(totales)),(-4,-1), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t_items._argW[0]=cmToPx(1)
    t_items._argW[2]=cmToPx(2)
    t_items._argW[3]=cmToPx(2)
    t_items._argW[4]=cmToPx(2)
    t_items._argW[5]=cmToPx(2)
    t_items._argW[6]=cmToPx(2)
    t_items._argW[7]=cmToPx(2.5)
    t_items._argW[8]=cmToPx(2.5)
    t_items._argW[9]=cmToPx(0.5)

    data = []

    for dato in TablaTotales:
        fila = []
        fila.append(parrafoCentro(" ", fuenteBase))
        fila.append(parrafoDerecha(dato[0], fuenteBase, tipo='Bold'))
        if dato[0]=='Descuento Extra':
            fila.append(parrafoDerecha("%s -%s" % (simbolo, dato[1]), fuenteBase, color='red'))        
        elif dato[0]=='Total':
            fila.append(parrafoDerecha("%s %s" % (simbolo, dato[1]), fuenteBase, tamaño=9, tipo='Bold'))
        else:
            fila.append(parrafoDerecha("%s %s" % (simbolo, dato[1]), fuenteBase))        
        fila.append(parrafoCentro(" ", fuenteBase))

        data.append(fila)  

    totales = len(TablaTotales)

    t_totales=Table(
        data,
        style=[
            ('GRID',(1,0),(-2,-1),1,colors.black),
            ('BOX',(1,0),(-2,-1),2,colors.black),
            ('BACKGROUND', (1,0),(-3,-1), color),
            # ('GRID',(0,0),(-2,-(totales+1)),1,colors.black),
            # ('GRID',(6,-(totales)),(-3,-1),1,colors.black),
            # ('BOX',(0,0),(-2,-(totales+1)),2,colors.black),
            # ('BOX',(6,-(totales)),(-3,-1),2,colors.black),
            # ('BACKGROUND', (0, 0), (-2, 0), color),
            # ('BACKGROUND', (5, 1), (5, -(totales+1)), colors.lightgrey),
            # ('BACKGROUND', (6,-(totales)),(-4,-1), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t_totales._argW[1]=cmToPx(3.5)
    t_totales._argW[2]=cmToPx(2.5)
    t_totales._argW[3]=cmToPx(3)

    return t_items, t_totales

def generarCotizacionVenta(titulo, vertical, logo, pie_pagina, Cabecera, TablaEncabezado, TablaDatos, color, condiciones, TablaTotales, fuenteBase, moneda, observaciones):
    data_cabecera = dataCabeceraCotizacionVenta(Cabecera, fuenteBase)
    # data_tabla = dataCotizacionVenta(TablaEncabezado, TablaDatos, TablaTotales, fuenteBase, color, moneda)
    data_items, data_totales = dataCotizacionVenta(TablaEncabezado, TablaDatos, TablaTotales, fuenteBase, color, moneda)
    
    elementos = []
    elementos.append(parrafoCentro('SOLICITUD DE COTIZACIÓN DEL CLIENTE', fuenteBase, 12, 'Bold'))
    elementos.append(data_cabecera)
    
    elementos.append(vacio())

    elementos.append(data_items)
    elementos.append(vacio())
    elementos.append(
        bloque(
                [
                data_totales,
                ]
            )
        )
    elementos.append(vacio())

    elementos.append(
        bloque(
                [
                parrafoIzquierda('CONDICIONES:', fuenteBase, 10, 'Bold'),
                listaGuion(condiciones, fuenteBase, 9),
                ]
            )
        )
    elementos.append(vacio())

    if observaciones:
        elementos.append(
            bloque(
                    [
                    parrafoIzquierda('OBSERVACIONES:', fuenteBase, 10, 'Bold'),
                    listaGuion(observaciones.splitlines(), fuenteBase, 9),
                    ]
                )
            )
        elementos.append(vacio())

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf

