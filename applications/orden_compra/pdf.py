from applications.pdf import *

def dataOrdenCompra(TablaEncabezado, TablaDatos, fuenteBase, color):
    encabezado = []
    for encab in TablaEncabezado:
        encabezado.append(parrafoCentro(encab, fuenteBase, 8, 'Bold'))
    
    data = []
    data.append(encabezado)
    
    for dato in TablaDatos:
        fila = []
        fila.append(parrafoCentro(dato[0], fuenteBase, 7))
        fila.append(parrafoIzquierda(dato[1], fuenteBase, 7))
        fila.append(parrafoIzquierda(dato[2], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[3], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[4], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[5], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[6], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[7], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[8], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[9], fuenteBase, 7))
        fila.append(parrafoDerecha(dato[10], fuenteBase, 7))

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
    t._argW[4]=cmToPx(2.15)
    t._argW[5]=cmToPx(2.15)
    t._argW[6]=cmToPx(2.15)
    t._argW[7]=cmToPx(2.15)
    t._argW[8]=cmToPx(2.15)
    t._argW[9]=cmToPx(2.15)
    t._argW[10]=cmToPx(2.15)

    return t

def dataProveedor(proveedor, interlocutor, usuario, orden, fuenteBase):
    data = []
    fila = []
    fila.append(parrafoIzquierda('Razón Social:', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s' % (proveedor.nombre), fuenteBase))
    fila.append(parrafoIzquierda('RUC:', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s' % (proveedor.ruc), fuenteBase))
    data.append(fila)
    fila = []
    fila.append(parrafoIzquierda('Dirección:', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s' % (proveedor.direccion), fuenteBase))
    fila.append(parrafoIzquierda('Vendedor:', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s' % (interlocutor.nombres), fuenteBase))
    data.append(fila)
    fila = []
    fila.append(parrafoIzquierda('Atención:', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s %s' % (usuario.first_name, usuario.last_name), fuenteBase))
    fila.append(parrafoIzquierda('Tipo de Compra', fuenteBase, tipo='Bold'))
    fila.append(parrafoIzquierda('%s - %s' % (orden.get_internacional_nacional_display(), orden.get_incoterms_display()), fuenteBase))
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
    t._argW[0]=cmToPx(2.5)
    t._argW[2]=cmToPx(2.5)

    return t

def dataTotales(TablaTotales, simbolo, fuenteBase):
    data = []
    for dato in TablaTotales:
        fila = []
        fila.append(parrafoCentro(" ", fuenteBase))
        fila.append(parrafoCentro(" ", fuenteBase))
        fila.append(parrafoDerecha(dato[0], fuenteBase, tipo='Bold'))
        if dato[0]=='Descuento Extra':
            fila.append(parrafoDerecha("%s -%s" % (simbolo, dato[1]), fuenteBase, color='red'))        
        elif dato[0]=='Total':
            fila.append(parrafoDerecha("%s %s" % (simbolo, dato[1]), fuenteBase, tamaño=9, tipo='Bold'))
        else:
            fila.append(parrafoDerecha("%s %s" % (simbolo, dato[1]), fuenteBase))        

        data.append(fila)  

    t=Table(
        data,
        style=[
            ('GRID',(2,0),(-1,-1),1,colors.black),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER'),
            ('LEFTPADDING', (0,0),(0,-1), 0),
            ]
        )
    t._argW[0]=cmToPx(1)
    t._argW[2]=cmToPx(3.5)
    t._argW[3]=cmToPx(2.15)

    return t

def dataSociedad(sociedad, orden, fuenteBase):
    data = []
    fila = ['', '', parrafoCentro('RUC: %s' % sociedad.ruc, fuenteBase, tipo='Bold')]
    data.append(fila)
    fila = [parrafoCentro('FECHA DE ORDEN DE COMPRA', fuenteBase, tipo='Bold'), '', parrafoCentro('ORDEN DE COMPRA', fuenteBase, tipo='Bold')]
    data.append(fila)
    fila = [parrafoCentro('%s' % orden.fecha_orden.strftime('%d/%m/%Y'), fuenteBase, tipo='Bold'), '', parrafoCentro('%s' % orden.numero_orden_compra, fuenteBase, tipo='Bold')]
    data.append(fila)

    t=Table(
        data,
        style=[
            ('GRID',(0,1),(0,-1),1,colors.black),
            ('GRID',(-1,0),(-1,-1),1,colors.black),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t._argW[0]=cmToPx(5)
    t._argW[2]=cmToPx(5)

    return t

def generarOrdenCompra(titulo, vertical, logo, pie_pagina, sociedad, orden, proveedor, interlocutor, usuario, TablaEncabezado, TablaDatos, TablaTotales, color):
    fuenteBase = "ComicNeue"

    data_sociedad_tabla = dataSociedad(sociedad, orden, fuenteBase)
    data_proveedor_tabla = dataProveedor(proveedor, interlocutor, usuario, orden, fuenteBase)
    data_tabla = dataOrdenCompra(TablaEncabezado, TablaDatos, fuenteBase, color)
    data_totales = dataTotales(TablaTotales, orden.moneda.simbolo, fuenteBase)
    
    elementos = []
    elementos.append(data_sociedad_tabla)
    elementos.append(vacio())
    elementos.append(data_proveedor_tabla)
    elementos.append(vacio())
    
    elementos.append(data_tabla)
    elementos.append(vacio())
    elementos.append(data_totales)

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf


def generarMotivoAnulacionOrdenCompra(titulo, vertical, logo, pie_pagina, Texto, TablaEncabezado, TablaDatos, color):
    fuenteBase = "ComicNeue"

    data_tabla = dataOrdenCompra(TablaEncabezado, TablaDatos, fuenteBase, color)
    
    elementos = []
    elementos.append(parrafoIzquierda(Texto, fuenteBase, 10))
    elementos.append(vacio())
    
    elementos.append(data_tabla)

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf
