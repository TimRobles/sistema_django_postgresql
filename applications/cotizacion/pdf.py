from applications.pdf import *

def dataCotizacionVenta(TablaEncabezado, TablaDatos, fuenteBase, color):
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
        fila.append(parrafoDerecha(dato[4], fuenteBase))
        fila.append(parrafoDerecha(dato[5], fuenteBase))        
        fila.append(parrafoIzquierda(dato[6], fuenteBase))
        fila.append(parrafoIzquierda(dato[7], fuenteBase))
        fila.append(parrafoDerecha(dato[8], fuenteBase))
        fila.append(parrafoDerecha(dato[9], fuenteBase))
        fila.append(parrafoDerecha(dato[10], fuenteBase))

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
    t._argW[2]=cmToPx(2)
    t._argW[3]=cmToPx(2)

    return t

def generarCotizacionVenta(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color):
    fuenteBase = "ComicNeue"

    data_tabla = dataCotizacionVenta(TablaEncabezado, TablaDatos, fuenteBase, color)
    
    elementos = []
    elementos.append(parrafoIzquierda(Texto[0], fuenteBase, 10))
    elementos.append(vacio())    
    elementos.append(parrafoIzquierda(Texto[1], fuenteBase, 10))
    elementos.append(vacio())    
    elementos.append(parrafoIzquierda(Texto[2], fuenteBase, 10))
    elementos.append(vacio())
    
    elementos.append(data_tabla)

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf

