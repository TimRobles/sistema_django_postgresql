from applications.pdf import *

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

    t=Table(data, style=[('GRID',(0,0),(-1,-2),0.5,colors.black),
                        ('GRID',(-9,-2),(-7,-1),0.5,colors.black),
                        ('BOX',(0,0),(-1,-2),1,colors.black),
                        ('BOX',(0,0),(-1,0),1,colors.black),
                        ('BOX',(-9,-1),(-7,-1),1,colors.black), #Inicio(x,y), Fin(x+1,y+1),grosor,color
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

def generarReporteDeudas(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color):
    fuenteBase = "ComicNeue"

    data_tabla = dataDeudas(TablaEncabezado, TablaDatos, fuenteBase, color)
    elementos = []
    elementos.append(parrafoIzquierda(Texto, fuenteBase, 10))
    elementos.append(vacio(2.5))
    elementos.append(data_tabla)
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf