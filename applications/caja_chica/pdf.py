from applications.pdf import *
from django.contrib.humanize.templatetags.humanize import intcomma

def dataChequeSolicitar(recibos, datos, fuenteBase):
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

def generarChequeSolicitar(titulo, vertical, logo, pie_pagina, fecha, recibos, datos, color):
    fuenteBase = "ComicNeue"

    data_recibos = dataChequeSolicitar(recibos, datos, fuenteBase)
    
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

########################################################################

def dataChequePdf(recibos, datos, cheque, suma_vueltos, suma_vueltos_cambio, fuenteBase):
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

    for recibo in recibos:
        fila = []
        fila.append(parrafoIzquierda(recibo.tipo, fuenteBase))

        data_documentos = []
        try:
            if len(recibo.RequerimientoDocumento_requerimiento.all())>0:
                data_documentos.append([
                    parrafoCentro('Fecha', fuenteBase),
                    parrafoIzquierda('Documento', fuenteBase),
                    parrafoIzquierda('Establecimiento', fuenteBase),
                    parrafoDerecha('Monto', fuenteBase),
                    parrafoCentro('Imagen', fuenteBase),
                    ])
                for documento in recibo.RequerimientoDocumento_requerimiento.all():
                    fila_nested = []
                    fila_nested.append(parrafoCentro(documento.fecha.strftime('%d/%m/%Y'), fuenteBase))
                    fila_nested.append(parrafoIzquierda("%s %s" % (documento.get_tipo_display(), documento.numero), fuenteBase))
                    fila_nested.append(parrafoIzquierda(documento.establecimiento, fuenteBase))
                    fila_nested.append(parrafoDerecha('%s %s' % (documento.moneda.simbolo, documento.total_documento), fuenteBase))
                    if documento.voucher:
                        fila_nested.append(parrafoCentro(hipervinculo(documento.voucher, 'Imagen de voucher'), fuenteBase))
                    else:
                        fila_nested.append(vacio())
                    data_documentos.append(fila_nested)
                    t_documentos=Table(
                        data_documentos,
                        style=[
                            ('GRID',(0,0),(-1,-1),1,colors.black),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('ALIGN',(0,0),(-1,-1),'CENTER')
                            ]
                        )
        except:
            data_documentos = []

        try:
            link = hipervinculo(recibo.voucher, 'Imagen de voucher')
            
            fila.append(parrafoIzquierda(recibo.concepto.__str__() + ' (' + link + ')', fuenteBase))
        except:
            try:
                if data_documentos != []:
                    fila.append(parrafoIzquierdaTabla(recibo.concepto.__str__(), t_documentos, fuenteBase))
                else:
                    fila.append(parrafoIzquierda(recibo.concepto.__str__(), fuenteBase))
            except:
                fila.append(parrafoIzquierda(recibo.concepto.__str__(), fuenteBase))
        
        fila.append(parrafoCentro(recibo.fecha.strftime('%d/%m/%Y'), fuenteBase))

        try:
            fila.append(parrafoCentro(recibo.fecha_pago.strftime('%d/%m/%Y'), fuenteBase))
        except:
            fila.append(parrafoCentro(recibo.fecha_entrega.strftime('%d/%m/%Y'), fuenteBase))

        fila.append(parrafoDerecha(recibo.simbolo + ' ' + intcomma(recibo.monto), fuenteBase))
        try:
            fila.append(parrafoDerecha(recibo.simbolo + ' ' + intcomma(recibo.mora), fuenteBase))
        except:
            fila.append(parrafoDerecha(recibo.simbolo + ' 0.00', fuenteBase))
        fila.append(parrafoDerecha(recibo.simbolo + ' ' + intcomma(recibo.redondeo), fuenteBase))
        fila.append(parrafoDerecha(recibo.simbolo + ' ' + intcomma(recibo.monto_pagado), fuenteBase))
        fila.append(parrafoCentro(recibo.get_estado_display(), fuenteBase))
        
        data_recibos.append(fila)

    fila = []
    fila.append(vacio())
    fila.append(vacio())
    fila.append(vacio())
    fila.append(parrafoDerecha("Total:", fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(datos['simbolo'] + ' ' + intcomma(datos['total']), fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(datos['simbolo'] + ' ' + intcomma(datos['total_mora']), fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(datos['simbolo'] + ' ' + intcomma(datos['total_redondeo']), fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(datos['simbolo'] + ' ' + intcomma(datos['total_pagado']), fuenteBase, 8, 'Bold'))
    
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
        parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(cheque.monto_cheques), fuenteBase),
        parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(datos['total_pagado']), fuenteBase),
        parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(cheque.redondeo), fuenteBase),
        parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(cheque.vuelto), fuenteBase),
        parrafoCentro(cheque.moneda.simbolo + ' ' + intcomma(suma_vueltos) + ' = ' + suma_vueltos_cambio[1] + ' ' + intcomma(suma_vueltos_cambio[0]), fuenteBase),
    ])
    
    return data_recibos, data_cheques, data_resumen_cheques

def generarChequePdf(titulo, vertical, logo, pie_pagina, fecha, recibos, datos, cheque, suma_vueltos, suma_vueltos_cambio, color):
    fuenteBase = "ComicNeue"

    data_recibos, data_cheques, data_resumen_cheques = dataChequePdf(recibos, datos, cheque, suma_vueltos, suma_vueltos_cambio, fuenteBase)

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
    elementos.append(parrafoIzquierda("Lima %s" % fecha, fuenteBase, 8))
    
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

########################################################################

def dataCajaChicaPdf(movimientos, caja, fuenteBase):
    encabezado = []
    encabezado.append(parrafoCentro("Fecha", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Concepto", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Ingresos", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Egresos", fuenteBase, 8, 'Bold'))
    encabezado.append(parrafoCentro("Saldo", fuenteBase, 8, 'Bold'))
    
    data = []
    data.append(encabezado)

    for movimiento in movimientos:
        fila = []
        fila.append(parrafoCentro(movimiento[0].strftime('%d/%m/%Y'), fuenteBase))

        data_documentos = []
        try:
            if len(movimiento[7]) > 0:
                data_documentos.append([
                    parrafoCentro('Fecha', fuenteBase),
                    parrafoIzquierda('Documento', fuenteBase),
                    parrafoIzquierda('Establecimiento', fuenteBase),
                    parrafoDerecha('Monto', fuenteBase),
                    parrafoCentro('Imagen', fuenteBase),
                    ])
                for documento in movimiento[7]:
                    fila_nested = []
                    fila_nested.append(parrafoCentro(documento.fecha.strftime('%d/%m/%Y'), fuenteBase))
                    fila_nested.append(parrafoIzquierda("%s %s" % (documento.get_tipo_display(), documento.numero), fuenteBase))
                    fila_nested.append(parrafoIzquierda(documento.establecimiento, fuenteBase))
                    fila_nested.append(parrafoDerecha('%s %s' % (documento.moneda.simbolo, documento.total_documento), fuenteBase))
                    if documento.voucher:
                        fila_nested.append(parrafoCentro(hipervinculo(documento.voucher, 'Imagen de voucher'), fuenteBase))
                    else:
                        fila_nested.append(vacio())
                    data_documentos.append(fila_nested)
                    t_documentos=Table(
                        data_documentos,
                        style=[
                            ('GRID',(0,0),(-1,-1),1,colors.black),
                            ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                            ('VALIGN',(0,0),(-1,-1),'TOP'),
                            ('ALIGN',(0,0),(-1,-1),'CENTER')
                            ]
                        )
        except:
            data_documentos = []

        try:
            if data_documentos != []:
                fila.append(parrafoIzquierdaTabla(movimiento[1], t_documentos, fuenteBase))
            else:
                fila.append(parrafoIzquierda(movimiento[1], fuenteBase))
        except:
            fila.append(parrafoIzquierda(movimiento[1], fuenteBase))
        fila.append(parrafoDerecha(caja.moneda.simbolo + ' ' + intcomma(movimiento[3]), fuenteBase))
        fila.append(parrafoDerecha(caja.moneda.simbolo + ' ' + intcomma(movimiento[4]), fuenteBase))
        fila.append(parrafoDerecha(caja.moneda.simbolo + ' ' + intcomma(movimiento[5]), fuenteBase))
        
        data.append(fila)

    fila = []
    fila.append(vacio())
    fila.append(vacio())
    fila.append(parrafoDerecha(caja.moneda.simbolo + ' ' + intcomma(caja.ingresos), fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(caja.moneda.simbolo + ' ' + intcomma(caja.egresos), fuenteBase, 8, 'Bold'))
    fila.append(parrafoDerecha(caja.moneda.simbolo + ' ' + intcomma(caja.saldo_final), fuenteBase, 8, 'Bold'))
    
    data.append(fila)

    return data

def generarCajaChicaPdf(titulo, vertical, logo, pie_pagina, movimientos, caja, color):
    fuenteBase = "ComicNeue"
    elementos = []
    elementos.append(parrafoCentro(titulo, fuenteBase, 12, 'Bold'))
    elementos.append(vacio())
    t=Table(
        dataCajaChicaPdf(movimientos, caja, fuenteBase),
        style=[
            ('GRID',(0,0),(-1,-2),1,colors.black),
            ('BOX',(0,0),(-1,-2),2,colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), color),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(-1,-1),'CENTER')
            ]
        )
    t._argW[0]=cmToPx(2)
    t._argW[2]=cmToPx(2)
    t._argW[3]=cmToPx(2)
    t._argW[4]=cmToPx(2)
    elementos.append(t)

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

def dataTelecreditoPdf(recibos, datos, telecredito, fuenteBase):
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

def generarTelecreditoPdf(titulo, vertical, logo, pie_pagina, fecha, recibos, datos, telecredito, color):
    fuenteBase = "ComicNeue"

    data_recibos, data_telecreditos = dataTelecreditoPdf(recibos, datos, telecredito, fuenteBase)

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