from applications.pdf import *

def dataProveedor(proveedor, interlocutor, titulo_requerimiento, fecha, comentario, fuenteBase, sociedad):
    data = []
    fila = []
    fila.append(parrafoIzquierda('Fecha:', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s' % (fecha), fuenteBase))
    fila.append(parrafoIzquierda('Razón Social:', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s' % (sociedad.razon_social), fuenteBase))
    data.append(fila)
    fila = []
    fila.append(parrafoIzquierda('Sres:', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s' % (proveedor.nombre), fuenteBase))
    fila.append(parrafoIzquierda('RUC :', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s' % (sociedad.ruc), fuenteBase))
    data.append(fila)
    fila = []
    fila.append(parrafoIzquierda('Interlocutor:', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s' % (interlocutor.nombres), fuenteBase))
    data.append(fila)
    fila = []
    fila.append(parrafoIzquierda('Asunto:', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s' % (titulo_requerimiento), fuenteBase))
    data.append(fila)
    if comentario:
        fila = []
        fila.append(parrafoIzquierda('Comentario:', fuenteBase, tipo='Bold'))
        fila.append(parrafoIzquierda('%s' % (comentario), fuenteBase))
        data.append(fila)

    
    t=Table(
        data,
        style=[
            # ('GRID',(0,0),(-1,-1),1,colors.black),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('LEFTPADDING', (0,0),(0,-1), 0),
            ]
        )
    t._argW[0]=cmToPx(3)

    return t

def dataRequerimientoMaterialProveedor(TablaEncabezado, TablaDatos, fuenteBase, color):
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
        fila.append(parrafoCentro(dato[4], fuenteBase))
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
    t._argW[1]=cmToPx(2.5)
    t._argW[2]=cmToPx(2.5)
    t._argW[4]=cmToPx(2.5)
    t._argW[5]=cmToPx(2.5)

    return t


def generarRequerimientoMaterialProveedor(titulo, vertical, logo, pie_pagina, titulo_requerimiento, proveedor, interlocutor, fecha, comentario, TablaEncabezado, TablaDatos, color, sociedad):
    fuenteBase = "ComicNeue"

    data_proveedor_tabla = dataProveedor(proveedor, interlocutor, titulo_requerimiento, fecha, comentario, fuenteBase,sociedad)
    data_tabla = dataRequerimientoMaterialProveedor(TablaEncabezado, TablaDatos, fuenteBase, color)
    
    elementos = []
    elementos.append(parrafoCentro('SOLICITUD DE COTIZACIÓN', fuenteBase, 15, 'Bold'))
    elementos.append(vacio())
    elementos.append(data_proveedor_tabla)
    elementos.append(vacio())
    elementos.append(data_tabla)

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf

