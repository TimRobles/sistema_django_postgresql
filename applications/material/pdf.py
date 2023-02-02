from decimal import Decimal
from applications.pdf import *

def dataPrecioLista(EncabezadoDatos, TablaDatos, fuenteBase, color):
    data = []
    fila = []
    for encabezado in EncabezadoDatos:
        fila.append(parrafoCentro(encabezado, fuenteBase, 8, 'Bold'))
    data.append(fila)

    for dato in TablaDatos:
        fila = []
        fila.append(parrafoIzquierda(dato[0], fuenteBase, 8))
        fila.append(parrafoCentro(dato[1], fuenteBase, 8))
        try:
            fila.append(parrafoDerecha(f"$ {intcomma(dato[2].precio_lista.quantize(Decimal('0.01')))}", fuenteBase, 8))
        except:
            fila.append(parrafoDerecha("", fuenteBase, 8))
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
    t._argW[1]=cmToPx(3)
    t._argW[2]=cmToPx(3.5)
    
    return t

def generarPrecioLista(titulo, vertical, logo, pie_pagina, EncabezadoDatos, TablaDatos, color, fuenteBase):
    data_precio_lista = dataPrecioLista(EncabezadoDatos, TablaDatos, fuenteBase, color)
    
    elementos = []
    elementos.append(parrafoCentro(titulo, fuenteBase, 12, 'Bold'))
    elementos.append(vacio())
    elementos.append(data_precio_lista)

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf