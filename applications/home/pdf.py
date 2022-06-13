from applications.pdf import *

def dataPrueba(TablaEncabezado, TablaDatos, fuenteBase):
    encabezado = []
    for encab in TablaEncabezado:
        encabezado.append(parrafoCentro(encab, fuenteBase, 8, 'Bold'))
    
    data = []
    data.append(encabezado)
    
    for dato in TablaDatos:
        fila = []
        fila.append(parrafoIzquierda(dato[0], fuenteBase))
        fila.append(parrafoCentro(dato[1], fuenteBase))
        fila.append(parrafoDerecha(dato[2], fuenteBase))

        data.append(fila)

    return data

def generarPrueba(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color):
    fuenteBase = "ComicNeue"

    data_tabla = dataPrueba(TablaEncabezado, TablaDatos, fuenteBase)
    
    elementos = []
    elementos.append(parrafoIzquierda(Texto, fuenteBase, 8))
    elementos.append(vacio())
    t=Table(
        data_tabla,
        style=[
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    # t._argW[0]=cmToPx(2.8)
    elementos.append(t)

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf