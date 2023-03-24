from decimal import Decimal
from applications.pdf import *

def dataCabeceraIngresoReclamoGarantia(Cabecera, fuenteBase):
    data = []
    fila=[]
    fila.append(parrafoIzquierda('Nro. Ingreso', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['nro_ingreso_reclamo_garantia'], fuenteBase, 10))
    fila.append(parrafoDerecha('Lima, ' + Cabecera['fecha_ingreso'], fuenteBase, 10))
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
    data.append(fila)

    fila=[]
    fila.append(parrafoIzquierda('Observación', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    observacion = ""
    if Cabecera['observacion']:
        observacion = Cabecera['observacion']
    fila.append(parrafoIzquierda(observacion, fuenteBase, 10))
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
    t._argW[3]=cmToPx(3.8)
    t._argW[4]=cmToPx(0.5)
    t._argW[5]=cmToPx(5)

    return t

def dataIngresoReclamoGarantia(series, fuenteBase, color):
    data = []
    encabezado = []
    encabezado.append(parrafoCentro('Serie', fuenteBase))
    encabezado.append(parrafoCentro('Comentario', fuenteBase))
    encabezado.append(parrafoCentro('Documento de Compra', fuenteBase))
    data.append(encabezado)
    for dato in series:
        fila = []
        fila.append(parrafoCentro(dato.serie.serie_base, fuenteBase))
        fila.append(parrafoCentro(dato.comentario, fuenteBase))
        fila.append(parrafoCentro(f"{dato.documento.descripcion} {dato.documento.fecha.strftime('%d/%m/%Y')}", fuenteBase))
        data.append(fila)

    t_items=Table(
        data,
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )

    return t_items


def generarIngresoReclamoGarantia(titulo, vertical, logo, pie_pagina, Cabecera, TablaDatos, condiciones, color, fuenteBase):
    data_cabecera = dataCabeceraIngresoReclamoGarantia(Cabecera, fuenteBase)
    
    elementos = []
    elementos.append(parrafoCentro('INGRESO POR RECLAMO DE GARANTÍA', fuenteBase, 12, 'Bold'))
    elementos.append(vacio())
    elementos.append(data_cabecera)
    
    elementos.append(vacio())

    for producto, series in TablaDatos.items():
        elementos.append(parrafoCentro(producto.__str__(), fuenteBase, 12, 'Bold'))
        elementos.append(vacio())
        data_series = dataIngresoReclamoGarantia(series, fuenteBase, color)
        elementos.append(data_series)
        elementos.append(vacio())

    elementos.append(
        bloque(
                [
                parrafoIzquierda('CONDICIONES:', fuenteBase, 10, 'Bold'),
                listaGuion(condiciones, fuenteBase, 9),
                ]
            )
        )
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf


###################################################################################


def dataCabeceraSalidaReclamoGarantia(Cabecera, fuenteBase):
    data = []
    fila=[]
    fila.append(parrafoIzquierda('Nro. Salida', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    fila.append(parrafoIzquierda(Cabecera['nro_salida_garantia'], fuenteBase, 10))
    if Cabecera['fecha_salida'] == 'SIN FECHA':
        fila.append(parrafoDerecha('Lima, ' + Cabecera['fecha_salida'], fuenteBase, 10, 'Bold', 'red'))
    else:
        fila.append(parrafoDerecha('Lima, ' + Cabecera['fecha_salida'], fuenteBase, 10))
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
    data.append(fila)

    fila=[]
    fila.append(parrafoIzquierda('Observación', fuenteBase, 10, 'Bold'))
    fila.append(parrafoCentro(':', fuenteBase, 10, 'Bold'))
    observacion = ""
    if Cabecera['observacion']:
        observacion = Cabecera['observacion']
    fila.append(parrafoIzquierda(observacion, fuenteBase, 10))
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
    t._argW[3]=cmToPx(3.8)
    t._argW[4]=cmToPx(0.5)
    t._argW[5]=cmToPx(5)

    return t

def dataSalidaReclamoGarantia(series, fuenteBase, color):
    data = []
    encabezado = []
    encabezado.append(parrafoCentro('Serie', fuenteBase))
    encabezado.append(parrafoCentro('Solución', fuenteBase))
    encabezado.append(parrafoCentro('Comentario', fuenteBase))
    data.append(encabezado)
    for dato in series:
        fila = []
        fila.append(parrafoCentro(dato.serie_ingreso_reclamo_garantia_detalle.serie.serie_base, fuenteBase))
        fila.append(parrafoCentro(dato.get_tipo_analisis_display(), fuenteBase))
        if dato.serie_cambio:
            fila.append(parrafoCentro(f"SERIE DE CAMBIO: {dato.serie_cambio}\n{dato.comentario}", fuenteBase))
        else:
            fila.append(parrafoCentro(dato.comentario, fuenteBase))
        data.append(fila)

    t_items=Table(
        data,
        style=[
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )

    return t_items


def generarSalidaReclamoGarantia(titulo, vertical, logo, pie_pagina, Cabecera, TablaDatos, condiciones, color, fuenteBase):
    data_cabecera = dataCabeceraSalidaReclamoGarantia(Cabecera, fuenteBase)
    
    elementos = []
    elementos.append(parrafoCentro('SALIDA POR RECLAMO DE GARANTÍA', fuenteBase, 12, 'Bold'))
    elementos.append(vacio())
    elementos.append(data_cabecera)
    
    elementos.append(vacio())

    for producto, series in TablaDatos.items():
        elementos.append(parrafoCentro(producto.__str__(), fuenteBase, 12, 'Bold'))
        elementos.append(vacio())
        data_series = dataSalidaReclamoGarantia(series, fuenteBase, color)
        elementos.append(data_series)
        elementos.append(vacio())

    elementos.append(
        bloque(
                [
                parrafoIzquierda('CONDICIONES:', fuenteBase, 10, 'Bold'),
                listaGuion(condiciones, fuenteBase, 9),
                ]
            )
        )
    
    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf


###################################################################################