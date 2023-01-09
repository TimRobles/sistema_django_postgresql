from applications.pdf import *

def dataCabeceraSolicitudPrestamoMateriales(Cabecera, fuenteBase):
    data = []
    fila=[]
    fila.append(parrafoIzquierda('Nro. Prestamo', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['numero_prestamo'], fuenteBase, 10))
    fila.append(parrafoDerecha('Lima, ' + Cabecera['fecha_prestamo'], fuenteBase, 10))
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
    fila.append(parrafoIzquierda('Comentario', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['comentario'], fuenteBase, 10))
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
    t._argW[3]=cmToPx(2.5)
    t._argW[4]=cmToPx(0.5)
    

    return t

def dataSolicitudPrestamoMateriales(TablaEncabezado, TablaDatos, fuenteBase, color):
    encabezado = []
    for encab in TablaEncabezado:
        encabezado.append(parrafoCentro(encab, fuenteBase, 8, 'Bold'))
    
    data = []
    data.append(encabezado)
    
    for dato in TablaDatos:
        fila = []
        fila.append(parrafoCentro(dato[0], fuenteBase))
        fila.append(parrafoIzquierda(dato[1], fuenteBase))
        fila.append(parrafoCentro(dato[2], fuenteBase))
        fila.append(parrafoDerecha(dato[3], fuenteBase))
        fila.append(parrafoDerecha(dato[4], fuenteBase))

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
    t._argW[4]=cmToPx(6)

    return t

def generarSolicitudPrestamoMateriales(titulo, vertical, logo, pie_pagina, Cabecera, TablaEncabezado, TablaDatos, color):
    fuenteBase = "ComicNeue"
    data_cabecera = dataCabeceraSolicitudPrestamoMateriales(Cabecera, fuenteBase)
    data_tabla = dataSolicitudPrestamoMateriales(TablaEncabezado, TablaDatos, fuenteBase, color)
    elementos = []
    elementos.append(vacio())
    elementos.append(parrafoCentro('SOLICITUD DE PRÉSTAMO DE EQUIPOS', fuenteBase, 12, 'Bold'))
    elementos.append(data_cabecera)
    elementos.append(vacio(2.5))
    elementos.append(data_tabla)
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf

###########################################################################################

def dataCabeceraNotaSalidaSeries(TablaEncabezado, TablaDatos, fuenteBase, color):
    encabezado = []
    for encab in TablaEncabezado:
        encabezado.append(parrafoCentro(encab, fuenteBase, 8, 'Bold'))
    
    data = []
    data.append(encabezado)
    
    fila = []
    for dato in TablaDatos:
        fila.append(parrafoCentro(dato, fuenteBase))
        
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
    t._argW[1]=cmToPx(2.5)
    t._argW[3]=cmToPx(3)

    return t

def dataSerieNotaSalidaSeries(series, fuenteBase):
    data = []
    
    if len(series) % 3 != 0:
        for i in range(3 - (len(series) % 3)):
            series.append("")
        

    fila = []
    for dato in series:
        if len(fila) % 3 == 0 and len(fila) > 2:
            data.append(fila)
            fila = []
        fila.append(parrafoCentro(dato, fuenteBase))
    data.append(fila)

    t=Table(
        data,
        style=[
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    
    return t

def generarNotaSalidaSeries(titulo, vertical, logo, pie_pagina, texto_cabecera, TablaEncabezado, TablaDatos, series_final, color):
    fuenteBase = "ComicNeue"
    data_cabecera = dataCabeceraNotaSalidaSeries(TablaEncabezado, TablaDatos, fuenteBase, color)
    elementos = []
    elementos.append(parrafoCentro(titulo, fuenteBase, 12, 'Bold'))
    elementos.append(vacio())
    elementos.append(parrafoIzquierda(texto_cabecera, fuenteBase, 10))
    elementos.append(vacio())
    elementos.append(data_cabecera)
    elementos.append(vacio())
    for producto, series in series_final.items():
        elementos.append(parrafoCentro(producto, fuenteBase, 10, 'Bold'))
        elementos.append(vacio())
        elementos.append(dataSerieNotaSalidaSeries(series, fuenteBase))
        elementos.append(vacio(1.5))
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf