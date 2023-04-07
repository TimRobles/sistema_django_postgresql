from decimal import Decimal
from applications.pdf import *

def dataTelecreditoReciboBoletaPago(EncabezadoDatos, TablaDatos, fuenteBase, color):
    data = []
    fila = []
    for encabezado in EncabezadoDatos:
        fila.append(parrafoCentro(encabezado, fuenteBase, 8, 'Bold'))
    data.append(fila)

    for dato in TablaDatos:
        fila = []
        fila.append(parrafoIzquierda(dato[0], fuenteBase, 8))
        fila.append(parrafoIzquierda(dato[1], fuenteBase, 8))
        fila.append(parrafoCentro(dato[2], fuenteBase, 8))
        fila.append(parrafoCentro(dato[3], fuenteBase, 8))
        data.append(fila)

    t=Table(
        data,
        style=[
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t._argW[0]=cmToPx(1)
    t._argW[2]=cmToPx(3)
    t._argW[3]=cmToPx(3.5)
    
    return t


def generarTelecreditoReciboBoletaPago(titulo, vertical, logo, pie_pagina, EncabezadoDatos, TablaDatos, color, fuenteBase):
    data_telecredito_recibos = dataTelecreditoReciboBoletaPago(EncabezadoDatos, TablaDatos, fuenteBase, color)
    
    elementos = []
    elementos.append(parrafoCentro(titulo, fuenteBase, 12, 'Bold'))
    elementos.append(vacio())
    elementos.append(data_telecredito_recibos)

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf