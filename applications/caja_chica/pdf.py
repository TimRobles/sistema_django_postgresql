from applications.pdf import *
from django.contrib.humanize.templatetags.humanize import intcomma

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