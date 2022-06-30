from applications.pdf import *

def dataPrueba(TablaEncabezado, TablaDatos, fuenteBase, color):
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

    filaExtra=[]
    filaExtra.append(parrafoIzquierda("jfalksjdflaksjdlfajsldfkjalsdkfjalskdjflaksdjflaksjdflkajsdlkfjasd", fuenteBase))
    filaExtra.append(parrafoCentro("jfalksjdflaksjdlfajsldfkjalsdkfjalskdjflaksdjflaksjdflkajsdlkfjasd", fuenteBase))
    filaExtra.append(parrafoDerecha("jfalksjdflaksjdlfajsldfkjalsdkfjalskdjflaksdjflaksjdflkajsdlkfjasd", fuenteBase))
    data.append(filaExtra)    

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
    t._argW[0]=cmToPx(3)
    t._argW[1]=cmToPx(5)

    return t

def generarPrueba(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color):
    fuenteBase = "ComicNeue"

    data_tabla = dataPrueba(TablaEncabezado, TablaDatos, fuenteBase, color)
    
    elementos = []
    elementos.append(parrafoIzquierda(Texto, fuenteBase, 8))
    elementos.append(vacio())
    
    elementos.append(data_tabla)

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf