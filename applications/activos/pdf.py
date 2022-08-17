from applications.pdf import *

def dataAsignacionActivos(TablaEncabezado, TablaDatos, fuenteBase, color):
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
        fila.append(parrafoIzquierda(dato[3], fuenteBase))
        fila.append(parrafoIzquierda(dato[4], fuenteBase))
        fila.append(parrafoDerecha(dato[5], fuenteBase))

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
    t._argW[4]=cmToPx(2.5)
    # t._argW[5]=cmToPx(2.5)

    return t


def dataFirmasAsignacionActivos(tabla_firmas, fuenteBase):
    data = []
    for dato_fila in tabla_firmas:
        fila = []
        for dato in dato_fila:
            # type(dato_fila[1][1])
            fila.append(parrafoCentro(dato, fuenteBase))
        data.append(fila)

    t = Table(
        data,
        style = [
            # ('GRID',(0,0),(-1,-1),1,colors.black),
            # ('BOX',(0,0),(-1,-1),2,colors.black),
            # ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    return t


def generarAsignacionActivos(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color, tabla_firmas):
    fuenteBase = "ComicNeue"

    data_tabla = dataAsignacionActivos(TablaEncabezado, TablaDatos, fuenteBase, color)
    data_firmas = dataFirmasAsignacionActivos(tabla_firmas, fuenteBase)
    elementos = []
    elementos.append(parrafoIzquierda(Texto[0], fuenteBase, 10))
    elementos.append(vacio(2.5))
    elementos.append(parrafoIzquierda(Texto[1], fuenteBase, 10))
    elementos.append(vacio(2))
    elementos.append(data_tabla)
    elementos.append(vacio(3))
    elementos.append(parrafoIzquierda(Texto[2], fuenteBase, 10))
    elementos.append(vacio(7))
    elementos.append(data_firmas)
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf