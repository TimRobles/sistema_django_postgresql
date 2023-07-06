from decimal import Decimal
from applications.pdf import *
from django.contrib.humanize.templatetags.humanize import intcomma

def dataChequeSolicitar(movimientos, cheque, fuenteBase):
    encabezado = []
    encabezado.append(parrafoCentro("Tipo", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Concepto", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Fecha de Vencimiento", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Monto Solicitado", fuenteBase, 8, 'Bold'))
    
    data_recibos = []
    data_recibos.append(encabezado)

    total = Decimal('0.00')
    for recibo in movimientos:
        fila = []
        fila.append(parrafoIzquierda(recibo[0], fuenteBase)) #Tipo
        if recibo[1]:
            link = hipervinculo(recibo[1], 'Imagen de recibo') #Foto recibo
            fila.append(parrafoIzquierda(recibo[2].__str__() + ' (' + link + ')', fuenteBase)) #Concepto y Foto recibo
        else:
            fila.append(parrafoIzquierda(recibo[2].__str__(), fuenteBase)) #Concepto

        fila.append(parrafoCentro(recibo[3].strftime('%d/%m/%Y'), fuenteBase)) #Fecha
        fila.append(parrafoDerecha(cheque.moneda.simbolo + ' ' + intcomma(recibo[4]), fuenteBase)) #Monto
        total += recibo[4]

        data_recibos.append(fila)

    fila = []
    fila.append(vacio())
    fila.append(vacio())
    fila.append(parrafoDerecha("Total:", fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(cheque.moneda.simbolo + ' ' + intcomma(total), fuenteBase, 8, 'Bold'))
    
    data_recibos.append(fila)

    return data_recibos

def generarChequeSolicitarPdf(titulo, vertical, logo, pie_pagina, fecha_hoy, movimientos, cheque, color):
    fuenteBase = "ComicNeue"

    data_recibos = dataChequeSolicitar(movimientos, cheque, fuenteBase)
    
    elementos = []
    elementos.append(parrafoIzquierda("Lima %s" % fecha_hoy, fuenteBase, 8))
    elementos.append(parrafoIzquierda("Gastos solicitados:", fuenteBase, 8))
    elementos.append(parrafoCentro(titulo, fuenteBase, 14, 'Bold'))
    elementos.append(vacio())
    t=Table(
        data_recibos,
        style=[
            ('GRID',(0,0),(-1,-2),1,colors.black),
            ('BOX',(0,0),(-1,-2),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t._argW[0]=cmToPx(2.8)
    t._argW[2]=cmToPx(2)
    t._argW[3]=cmToPx(2)
    elementos.append(t)

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf

########################################################################

def dataChequeCerrar(movimientos, cheque, fuenteBase):
    encabezado = []
    encabezado.append(parrafoCentro("Tipo", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Concepto", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Fecha de Vencimiento", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Fecha de Pago", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Monto Solicitado", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Mora", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Redondeo", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Monto Usado", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Estado", fuenteBase, 8, 'Bold'))

    data_recibos = []
    data_recibos.append(encabezado)

    total = Decimal('0.00')
    total_mora = Decimal('0.00')
    total_redondeo = Decimal('0.00')
    total_pagado = Decimal('0.00')

    for recibo in movimientos:
        fila = []
        fila.append(parrafoIzquierda(recibo[0], fuenteBase)) #Tipo

        data_documentos = []
        try:
            if recibo[7]: #Documentos
                data_documentos.append([
                    parrafoCentro('Fecha', fuenteBase),
                    parrafoIzquierda('Documento', fuenteBase),
                    parrafoIzquierda('Establecimiento', fuenteBase),
                    parrafoDerecha('Monto', fuenteBase),
                    parrafoCentro('Imagen', fuenteBase),
                    ])
                for documento in recibo[7]: #Documentos
                    fila_nested = []
                    fila_nested.append(parrafoCentro(documento.fecha.strftime('%d/%m/%Y'), fuenteBase))
                    fila_nested.append(parrafoIzquierda("%s %s" % (documento.get_tipo_display(), documento.numero), fuenteBase))
                    fila_nested.append(parrafoIzquierda(documento.establecimiento, fuenteBase))
                    fila_nested.append(parrafoDerecha('%s %s' % (documento.moneda.simbolo, documento.total_documento), fuenteBase))
                    print(documento.voucher, documento)
                    if documento.voucher:
                        fila_nested.append(parrafoCentro(hipervinculo(documento.voucher, 'Imagen de voucher'), fuenteBase))
                    else:
                        fila_nested.append(vacio())
                    data_documentos.append(fila_nested)
                    print(data_documentos)
                    t_documentos=Table(
                        data_documentos,
                        style=[
                                ('GRID',(0,0),(-1,-1),1,colors.black),
                                ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                                ('VALIGN',(0,0),(-1,-1),'TOP'),
                                ('ALIGN',(0,0),(-1,-1),'CENTER')
                            ]
                        )
        except Exception as e:
            print(e)
            data_documentos = []

        if data_documentos != []:
            fila.append(parrafoIzquierdaTabla(recibo[2].__str__(), t_documentos, fuenteBase))
        elif recibo[8]:
            link = hipervinculo(recibo[8], 'Imagen de voucher')
            fila.append(parrafoIzquierda(recibo[2].__str__() + ' (' + link + ')', fuenteBase))
        else:
            fila.append(parrafoIzquierda(recibo[2].__str__(), fuenteBase))
        
        fila.append(parrafoCentro(recibo[3].strftime('%d/%m/%Y'), fuenteBase)) #Fecha

        fila.append(parrafoCentro(recibo[9].strftime('%d/%m/%Y'), fuenteBase)) #Fecha Pago
        
        fila.append(parrafoDerecha(cheque.moneda.simbolo + ' ' + intcomma(recibo[4]), fuenteBase))
        fila.append(parrafoDerecha(cheque.moneda.simbolo + ' ' + intcomma(recibo[5]), fuenteBase))
        fila.append(parrafoDerecha(cheque.moneda.simbolo + ' ' + intcomma(recibo[6]), fuenteBase))
        fila.append(parrafoDerecha(cheque.moneda.simbolo + ' ' + intcomma(recibo[10]), fuenteBase))
        fila.append(parrafoCentro(recibo[11], fuenteBase))
        
        total += recibo[4]
        total_mora += recibo[5]
        total_redondeo += recibo[6]
        total_pagado += recibo[10]

        data_recibos.append(fila)

    fila = []
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(parrafoDerecha("Total:", fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(cheque.moneda.simbolo + ' ' + intcomma(total), fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(cheque.moneda.simbolo + ' ' + intcomma(total_mora), fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(cheque.moneda.simbolo + ' ' + intcomma(total_redondeo), fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(cheque.moneda.simbolo + ' ' + intcomma(total_pagado), fuenteBase, 8, 'Bold'))
    
    data_recibos.append(fila)

    data_cheques = []
    data_cheques.append([
        parrafoCentro('Banco', fuenteBase, 8, 'Bold'),
        parrafoCentro('Número', fuenteBase, 8, 'Bold'),
        parrafoCentro('Monto', fuenteBase, 8, 'Bold'),
        parrafoCentro('Fecha de Emisión', fuenteBase, 8, 'Bold'),
        parrafoCentro('Fecha de Cobro', fuenteBase, 8, 'Bold'),
        parrafoCentro('Estado', fuenteBase, 8, 'Bold'),
        parrafoCentro('Foto', fuenteBase, 8, 'Bold'),
    ])

    for cheque_fisico in cheque.ChequeFisico_cheque.all():
        data_cheques.append([
            parrafoCentro(cheque_fisico.banco, fuenteBase),
            parrafoCentro(cheque_fisico.numero, fuenteBase),
            parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(cheque_fisico.monto), fuenteBase),
            parrafoCentro(cheque_fisico.fecha_emision.strftime('%d/%m/%Y'), fuenteBase),
            parrafoCentro(cheque_fisico.fecha_cobro.strftime('%d/%m/%Y'), fuenteBase),
            parrafoCentro(cheque_fisico.get_estado_display(), fuenteBase),
            parrafoCentro(hipervinculo(cheque_fisico.foto, os.path.basename(cheque_fisico.foto.name)), fuenteBase),
        ])

    data_resumen_cheques = []
    data_resumen_cheques.append([
        parrafoCentro('Monto en Cheques', fuenteBase, 8, 'Bold'),
        parrafoCentro('Monto Usado', fuenteBase, 8, 'Bold'),
        parrafoCentro('Redondeo', fuenteBase, 8, 'Bold'),
        parrafoCentro('Vuelto', fuenteBase, 8, 'Bold'),
        parrafoCentro('Otros Vueltos', fuenteBase, 8, 'Bold'),
    ])


    data_resumen_cheques.append([
        parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(cheque.recibido), fuenteBase),
        parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(total_pagado), fuenteBase),
        parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(cheque.redondeo), fuenteBase),
        parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(cheque.vuelto), fuenteBase),
        parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(Decimal('0.00')) + ' = ' + 'S/' + ' ' + intcomma(Decimal('0.00')), fuenteBase),
    ])
    
    return data_recibos, data_cheques, data_resumen_cheques

def generarChequeCerrarPdf(titulo, vertical, logo, pie_pagina, fecha_hoy, movimientos, cheque, color):
    fuenteBase = "ComicNeue"

    data_recibos, data_cheques, data_resumen_cheques = dataChequeCerrar(movimientos, cheque, fuenteBase)

    t_cheques=Table(
        data_cheques,
        style=[
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t_cheques._argW[0]=cmToPx(3)
    t_cheques._argW[1]=cmToPx(5)
    t_cheques._argW[2]=cmToPx(3)
    t_cheques._argW[3]=cmToPx(2)
    t_cheques._argW[4]=cmToPx(2)
    t_cheques._argW[5]=cmToPx(2)

    t_resumen_cheques=Table(
        data_resumen_cheques,
        style=[
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t_resumen_cheques._argW[0]=cmToPx(3)
    t_resumen_cheques._argW[1]=cmToPx(3)
    t_resumen_cheques._argW[2]=cmToPx(3)
    t_resumen_cheques._argW[3]=cmToPx(3)
    t_resumen_cheques._argW[4]=cmToPx(3)

    t_recibos=Table(
        data_recibos,
        style=[
            ('GRID',(0,0),(-1,-2),1,colors.black),
            ('BOX',(0,0),(-1,-2),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t_recibos._argW[0]=cmToPx(2.8)
    t_recibos._argW[2]=cmToPx(2)
    t_recibos._argW[3]=cmToPx(2)
    t_recibos._argW[4]=cmToPx(2)
    t_recibos._argW[5]=cmToPx(2)
    t_recibos._argW[6]=cmToPx(2)
    t_recibos._argW[7]=cmToPx(2)
    t_recibos._argW[8]=cmToPx(2)

    elementos = []
    elementos.append(parrafoIzquierda("Lima %s" % fecha_hoy, fuenteBase, 8))
    
    elementos.append(parrafoCentro("Datos del cheque", fuenteBase, 14, 'Bold'))
    elementos.append(vacio())
    elementos.append(t_cheques)
    elementos.append(vacio())
    elementos.append(t_resumen_cheques)

    elementos.append(vacio())
    elementos.append(parrafoIzquierda("Gastos Realizados:", fuenteBase, 8))
    elementos.append(parrafoCentro(titulo, fuenteBase, 10, 'Bold'))
    elementos.append(vacio())
    
    elementos.append(t_recibos)
    

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf

#######################################################################

def dataTelecreditoSolicitar(recibos, datos, fuenteBase):
    encabezado = []
    encabezado.append(parrafoCentro("Tipo", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Concepto", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Fecha de Vencimiento", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Monto Solicitado", fuenteBase, 8, 'Bold'))
    
    data_recibos = []
    data_recibos.append(encabezado)

    for recibo in recibos:
        fila = []
        fila.append(parrafoIzquierda(recibo.tipo, fuenteBase))
        try:
            link = hipervinculo(recibo.foto, 'Imagen de recibo')
            
            fila.append(parrafoIzquierda(recibo.concepto.__str__() + ' (' + link + ')', fuenteBase))
        except:
            fila.append(parrafoIzquierda(recibo.concepto.__str__(), fuenteBase))

        fila.append(parrafoCentro(recibo.fecha.strftime('%d/%m/%Y'), fuenteBase))
        fila.append(parrafoDerecha(recibo.simbolo + ' ' + intcomma(recibo.monto), fuenteBase))

        data_recibos.append(fila)

    fila = []
    fila.append(vacio())
    fila.append(vacio())
    fila.append(parrafoDerecha("Total:", fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(datos['simbolo'] + ' ' + intcomma(datos['total']), fuenteBase, 8, 'Bold'))
    
    data_recibos.append(fila)

    return data_recibos

def generarTelecreditoSolicitar(titulo, vertical, logo, pie_pagina, fecha, recibos, datos, color):
    fuenteBase = "ComicNeue"

    data_recibos = dataTelecreditoSolicitar(recibos, datos, fuenteBase)
    
    elementos = []
    elementos.append(parrafoIzquierda("Lima %s" % fecha, fuenteBase, 8))
    elementos.append(parrafoIzquierda("Gastos solicitados:", fuenteBase, 8))
    elementos.append(parrafoCentro(titulo, fuenteBase, 14, 'Bold'))
    elementos.append(vacio())
    t=Table(
        data_recibos,
        style=[
            ('GRID',(0,0),(-1,-2),1,colors.black),
            ('BOX',(0,0),(-1,-2),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t._argW[0]=cmToPx(2.8)
    t._argW[2]=cmToPx(2)
    t._argW[3]=cmToPx(2)
    elementos.append(t)

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf
    
#######################################################################

def dataTelecreditoCerrar(recibos, datos, telecredito, fuenteBase):
    encabezado = []
    encabezado.append(parrafoCentro("Tipo", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Concepto", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Fecha de Vencimiento", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Fecha de Pago", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Monto Solicitado", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Monto Usado", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Estado", fuenteBase, 8, 'Bold'))

    data_recibos = []
    data_recibos.append(encabezado)

    for recibo in recibos:
        fila = []
        fila.append(parrafoIzquierda(recibo.tipo, fuenteBase))

        fila.append(parrafoIzquierda(recibo.concepto, fuenteBase))
        fila.append(parrafoCentro(recibo.fecha.strftime('%d/%m/%Y'), fuenteBase))
        fila.append(parrafoCentro(recibo.fecha_pago.strftime('%d/%m/%Y'), fuenteBase))
        fila.append(parrafoDerecha(recibo.simbolo + ' ' + intcomma(recibo.monto), fuenteBase))
        fila.append(parrafoDerecha(recibo.simbolo + ' ' + intcomma(recibo.monto_pagado), fuenteBase))
        fila.append(parrafoCentro(recibo.get_estado_display(), fuenteBase))
        
        data_recibos.append(fila)

    fila = []
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(parrafoDerecha("Total:", fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(datos['simbolo'] + ' ' + intcomma(datos['total']), fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(datos['simbolo'] + ' ' + intcomma(datos['total_pagado']), fuenteBase, 8, 'Bold'))
    
    data_recibos.append(fila)

    data_telecreditos = []
    data_telecreditos.append([
        parrafoCentro('Banco', fuenteBase, 8, 'Bold'),
        parrafoCentro('Número', fuenteBase, 8, 'Bold'),
        parrafoCentro('Monto', fuenteBase, 8, 'Bold'),
        parrafoCentro('Fecha de Emisión', fuenteBase, 8, 'Bold'),
        parrafoCentro('Fecha de Cobro', fuenteBase, 8, 'Bold'),
        parrafoCentro('Estado', fuenteBase, 8, 'Bold'),
        parrafoCentro('Foto', fuenteBase, 8, 'Bold'),
    ])

    data_telecreditos.append([
        parrafoCentro(telecredito.banco, fuenteBase),
        parrafoCentro(telecredito.numero, fuenteBase),
        parrafoCentro(telecredito.moneda.simbolo + ' ' + intcomma(telecredito.monto), fuenteBase),
        parrafoCentro(telecredito.fecha_emision.strftime('%d/%m/%Y'), fuenteBase),
        parrafoCentro(telecredito.fecha_cobro.strftime('%d/%m/%Y'), fuenteBase),
        parrafoCentro(telecredito.get_estado_display(), fuenteBase),
        parrafoCentro(hipervinculo(telecredito.foto, os.path.basename(telecredito.foto.name)), fuenteBase),
    ])

    return data_recibos, data_telecreditos

def generarTelecreditoCerrar(titulo, vertical, logo, pie_pagina, fecha, recibos, datos, telecredito, color):
    fuenteBase = "ComicNeue"

    data_recibos, data_telecreditos = dataTelecreditoCerrar(recibos, datos, telecredito, fuenteBase)

    t_telecreditos=Table(
        data_telecreditos,
        style=[
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ('BOX',(0,0),(-1,-1),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t_telecreditos._argW[0]=cmToPx(3)
    t_telecreditos._argW[1]=cmToPx(5)
    t_telecreditos._argW[2]=cmToPx(3)
    t_telecreditos._argW[3]=cmToPx(2)
    t_telecreditos._argW[4]=cmToPx(2)
    t_telecreditos._argW[5]=cmToPx(2)

    t_recibos=Table(
        data_recibos,
        style=[
            ('GRID',(0,0),(-1,-2),1,colors.black),
            ('BOX',(0,0),(-1,-2),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t_recibos._argW[0]=cmToPx(2.8)
    t_recibos._argW[2]=cmToPx(2)
    t_recibos._argW[3]=cmToPx(2)
    t_recibos._argW[4]=cmToPx(2)
    t_recibos._argW[5]=cmToPx(2)
    t_recibos._argW[6]=cmToPx(2)

    elementos = []
    elementos.append(parrafoIzquierda("Lima %s" % fecha, fuenteBase, 8))
    
    elementos.append(parrafoCentro("Datos del telecredito", fuenteBase, 14, 'Bold'))
    elementos.append(vacio())
    elementos.append(t_telecreditos)

    elementos.append(vacio())
    elementos.append(parrafoIzquierda("Gastos Realizados:", fuenteBase, 8))
    elementos.append(parrafoCentro(titulo, fuenteBase, 10, 'Bold'))
    elementos.append(vacio())
    
    elementos.append(t_recibos)
    

    buf = generarPDF(titulo, elementos, vertical, logo, pie_pagina)

    return buf