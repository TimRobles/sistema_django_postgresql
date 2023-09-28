from django.shortcuts import render
import time
from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from applications.comprobante_compra.models import ComprobanteCompraPIDetalle
from applications.funciones import numeroXn
from applications.importaciones import *
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Alignment
from openpyxl.styles import *
from openpyxl.styles.borders import Border, Side
from openpyxl.chart import Reference, Series,LineChart
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.plotarea import DataTable
from applications.material.models import Material
from applications.movimiento_almacen.managers import ordenar_movimientos
from applications.movimiento_almacen.models import MovimientosAlmacen
from applications.reportes.funciones import *
from applications.datos_globales.models import DocumentoFisico, Moneda, TipoCambioSunat
from applications.home.templatetags.funciones_propias import get_enlace_nubefact, redondear
from applications.comprobante_venta.models import BoletaVenta, BoletaVentaDetalle, FacturaVenta, FacturaVentaDetalle
from applications.nota.models import NotaCredito
from applications.crm.models import ClienteCRMDetalle
from applications.clientes.models import CorreoInterlocutorCliente, RepresentanteLegalCliente, TelefonoInterlocutorCliente
from applications.datos_globales.models import Departamento, Moneda
from applications.cotizacion.models import CotizacionVenta

####################################################  FACTURACIÓN VS ASESOR COMERCIAL  ####################################################   

def ReporteFacturacionAsesorComercial(fecha_inicio, fecha_fin, asesor_comercial):
    list_comprobante = TIPO_COMPROBANTE 
    DICT_TIPO_COMPROBANTE = dict(list_comprobante)

    moneda_base = Moneda.objects.get(simbolo='$')

    if asesor_comercial:
        asesores = get_user_model().objects.filter(id=asesor_comercial)
    else:
        asesores = get_user_model().objects.filter(id__in = [cotizacion.vendedor.id for cotizacion in CotizacionVenta.objects.all()])

    wb = Workbook()
    data_resumen = []
    total_resumen = Decimal('0.00')
    count = 0
    for asesor_comercial in asesores:
        fila_resumen = []
        data = []
        data_nota = []

        notas_credito = NotaCredito.objects.filter(estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin)

        total_nota= Decimal('0.00')
        total_nota_factura = Decimal('0.00')
        total_factura = Decimal('0.00')
        for factura in FacturaVenta.objects.filter(confirmacion__cotizacion_venta__vendedor=asesor_comercial, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin).order_by("fecha_emision"):
            if factura.moneda == moneda_base:
                total_factura += factura.total
            else:
                total_factura += (factura.total / factura.tipo_cambio).quantize(Decimal('0.01'))

            fila = []
            if asesor_comercial.first_name:
                fila.append(f"{asesor_comercial.first_name} {asesor_comercial.last_name}")
            else:
                fila.append(asesor_comercial.username)
            fila.append(factura.fecha_emision.strftime('%d/%m/%Y'))
            fila.append(DICT_TIPO_COMPROBANTE[factura.tipo_comprobante])
            fila.append(f"{str(factura.serie_comprobante.serie)} - {str(factura.numero_factura).zfill(6)}")
            fila.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(factura.total))))
            data.append(fila)

        for factura_nota in FacturaVenta.objects.filter(confirmacion__cotizacion_venta__vendedor=asesor_comercial):
            fila_nota = []
            for nota in notas_credito:
                if nota.content_type_documento==DocumentoFisico.objects.get(modelo=ContentType.objects.get_for_model(FacturaVenta)) and nota.id_registro_documento==factura_nota.id:
                    if nota.moneda == moneda_base:
                        total_nota_factura += nota.total
                    else:
                        total_nota_factura += (nota.total / nota.tipo_cambio).quantize(Decimal('0.01'))
                    if asesor_comercial.first_name:
                        fila_nota.append(f"{asesor_comercial.first_name} {asesor_comercial.last_name}")
                    else:
                        fila_nota.append(asesor_comercial.username)
                    fila_nota.append(nota.fecha_emision.strftime('%d/%m/%Y'))
                    fila_nota.append(DICT_TIPO_COMPROBANTE[nota.tipo_comprobante])
                    fila_nota.append(f"{str(nota.serie_comprobante.serie)} - {str(nota.numero_nota).zfill(6)}")
                    fila_nota.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(nota.total))))
                    data_nota.append(fila_nota)

        total_nota_boleta = Decimal('0.00')
        total_boleta = Decimal('0.00')
        for boleta in BoletaVenta.objects.filter(confirmacion__cotizacion_venta__vendedor=asesor_comercial, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin).order_by("fecha_emision"):
            if boleta.moneda == moneda_base:
                total_boleta += boleta.total
            else:
                total_boleta += (boleta.total / boleta.tipo_cambio).quantize(Decimal('0.01'))

            fila = []
            if asesor_comercial.first_name:
                fila.append(f"{asesor_comercial.first_name} {asesor_comercial.last_name}")
            else:
                fila.append(asesor_comercial.username)
            fila.append(boleta.fecha_emision.strftime('%d/%m/%Y'))
            fila.append(DICT_TIPO_COMPROBANTE[boleta.tipo_comprobante])
            fila.append(f"{str(boleta.serie_comprobante.serie)} - {str(boleta.numero_boleta).zfill(6)}")
            fila.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(boleta.total))))
            data.append(fila)

        for boleta_nota in BoletaVenta.objects.filter(confirmacion__cotizacion_venta__vendedor=asesor_comercial):
            fila_nota = []
            for nota in notas_credito:
                if nota.content_type_documento==DocumentoFisico.objects.get(modelo=ContentType.objects.get_for_model(BoletaVenta)) and nota.id_registro_documento==boleta_nota.id:
                    if nota.moneda == moneda_base:
                        total_nota_boleta += nota.total
                    else:
                        total_nota_boleta += (nota.total / nota.tipo_cambio).quantize(Decimal('0.01'))

                    if asesor_comercial.first_name:
                        fila_nota.append(f"{asesor_comercial.first_name} {asesor_comercial.last_name}")
                    else:
                        fila_nota.append(asesor_comercial.username)
                    fila_nota.append(nota.fecha_emision.strftime('%d/%m/%Y'))
                    fila_nota.append(DICT_TIPO_COMPROBANTE[nota.tipo_comprobante])
                    fila_nota.append(f"{str(nota.serie_comprobante.serie)} - {str(nota.numero_nota).zfill(6)}")
                    fila_nota.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(nota.total))))
                    data_nota.append(fila_nota)

        total = total_factura + total_boleta
        total_nota = total_nota_factura + total_nota_boleta
        total_total = total - total_nota
        list_encabezado = [
            'Asesor Comercial',
            'Fecha Emisión',
            'Tipo Comprobante',
            'N° Comprobante',
            'Total',
            ]
        
        if data != []:
            if count != 0:
                hoja = wb.create_sheet(str(asesor_comercial.username))

            else:
                hoja = wb.active
                hoja.title = str(asesor_comercial.username)
                # count += 1 

            data.sort(key = lambda i: i[1], reverse=False)
            # data.append(["","","SUBTOTAL",("%s %s" % (moneda_base.simbolo, intcomma(redondear(total))))])
            
            hoja.append(tuple(list_encabezado))

            col_range = hoja.max_column  # get max columns in the worksheet
            # cabecera de la tabla
            for col in range(1, col_range + 1):
                cell_header = hoja.cell(1, col)
                cell_header.fill = RELLENO_EXCEL
                cell_header.font = NEGRITA

            for fila in data:
                hoja.append(fila)

            for row in hoja.rows:
                for col in range(hoja.max_column):
                    row[col].border = BORDE_DELGADO
                    if col == 1 or col==3:
                        row[col].alignment = ALINEACION_CENTRO
                    elif col == 4:
                        row[col].alignment = ALINEACION_DERECHA
            if data_nota != []:
                hoja.append(('', '', '','SUBTOTAL', ("%s %s" % (moneda_base.simbolo, intcomma(redondear(total))))))
            else:
                hoja.append(('', '', '','TOTAL', ("%s %s" % (moneda_base.simbolo, intcomma(redondear(total))))))

            nueva_fila = hoja.max_row

            for col in range(1, col_range + 1):
                if col == 4:
                    cell_header = hoja.cell(nueva_fila, col)
                    cell_header.fill = RELLENO_EXCEL
                    cell_header.font = NEGRITA
                elif col == 5:
                    cell_header = hoja.cell(nueva_fila, col)
                    cell_header.font = NEGRITA

            for i in range(hoja.max_row):
                if i >= nueva_fila-1:
                    row = list(hoja.rows)[i]
                    for col in range(hoja.max_column):
                        if col > 2:
                            row[col].border = BORDE_DELGADO
                            if col==3:
                                row[col].alignment = ALINEACION_CENTRO
                            elif col == 4:
                                row[col].alignment = ALINEACION_DERECHA

            if data_nota != []:
                data_nota.sort(key = lambda i: i[1], reverse=False)
                # data_nota.append(["","","SUBTOTAL",("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_nota))))])
                # cabecera de la tabla
                hoja.append(('',)) # Crea la fila del encabezado con los títulos
                hoja.append(tuple(list_encabezado))

                nueva_fila = hoja.max_row

                for col in range(1, col_range + 1):
                    cell_header = hoja.cell(nueva_fila, col)
                    cell_header.fill = RELLENO_EXCEL
                    cell_header.font = NEGRITA

                for fila in data_nota:
                    hoja.append(fila) # Crea la fila del encabezado con los títulos

                for i in range(hoja.max_row):
                    if i >= nueva_fila-1:
                        row = list(hoja.rows)[i]
                        for col in range(hoja.max_column):
                            row[col].border = BORDE_DELGADO
                            if col == 1 or col==3:
                                row[col].alignment = ALINEACION_CENTRO
                            elif col == 4:
                                row[col].alignment = ALINEACION_DERECHA

                hoja.append(('', '', '','SUBTOTAL', ("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_nota)))))) 

                nueva_fila = hoja.max_row

                for col in range(1, col_range + 1):
                    if col == 4:
                        cell_header = hoja.cell(nueva_fila, col)
                        cell_header.fill = RELLENO_EXCEL
                        cell_header.font = NEGRITA
                    elif col == 5:
                        cell_header = hoja.cell(nueva_fila, col)
                        cell_header.font = NEGRITA

                for i in range(hoja.max_row):
                    if i >= nueva_fila-1:
                        row = list(hoja.rows)[i]
                        for col in range(hoja.max_column):
                            if col > 2:
                                row[col].border = BORDE_DELGADO
                                if col==3:
                                    row[col].alignment = ALINEACION_CENTRO
                                elif col == 4:
                                    row[col].alignment = ALINEACION_DERECHA

                hoja.append(('',)) # Crea la fila del encabezado con los títulos
                hoja.append(('', '', '','TOTAL', ("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_total)))))) 

                nueva_fila = hoja.max_row

                for col in range(1, col_range + 1):
                    if col == 4:
                        cell_header = hoja.cell(nueva_fila, col)
                        cell_header.fill = RELLENO_EXCEL
                        cell_header.font = NEGRITA
                    elif col == 5:
                        cell_header = hoja.cell(nueva_fila, col)
                        cell_header.font = NEGRITA

                for i in range(hoja.max_row):
                    if i >= nueva_fila-1:
                        row = list(hoja.rows)[i]
                        for col in range(hoja.max_column):
                            if col > 2:
                                row[col].border = BORDE_DELGADO
                                if col==3:
                                    row[col].alignment = ALINEACION_CENTRO
                                elif col == 4:
                                    row[col].alignment = ALINEACION_DERECHA
            
            total_resumen += total_total

            if asesor_comercial.first_name:
                fila_resumen.append(f"{asesor_comercial.first_name} {asesor_comercial.last_name}")
            else:
                fila_resumen.append(asesor_comercial.username)
            fila_resumen.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_total))))
            fila_resumen.append(total_total)
            data_resumen.append(fila_resumen)

        ajustarColumnasSheet(hoja)
        count += 1

    list_encabezado_resumen = [
        'Asesor Comercial',
        'Total',
        'Porcentaje',
        ]
    hoja = wb.create_sheet('RESUMEN')
    
    hoja.append(tuple(list_encabezado_resumen))

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = RELLENO_EXCEL
        cell_header.font = NEGRITA
    
    data_resumen.sort(key = lambda i: i[2], reverse=True)
    for fila in data_resumen:
        fila[2] = ("%s %s" % (intcomma(redondear((Decimal(fila[2])/total_resumen)*100)), '%'))

    for fila in data_resumen:
        hoja.append(fila)

    for row in hoja.rows:
        for col in range(hoja.max_column):
            row[col].border = BORDE_DELGADO
            if col == 1 or col == 2:
                row[col].alignment = ALINEACION_DERECHA

    ajustarColumnasSheet(hoja)
    return wb

####################################################  VENTAS VS DEPARTAMENTO  ####################################################   

def ReporteVentasDepartamento(titulo, fecha_inicio, fecha_fin, departamento_codigo):

    if departamento_codigo:
        departamentos = Departamento.objects.filter(codigo=departamento_codigo)
    else:
        departamentos = Departamento.objects.all()

    moneda_base = Moneda.objects.get(simbolo='$')

    wb = Workbook()
    data_resumen = []
    total_resumen = Decimal('0.00')
    count = 0
    for departamento in departamentos:
        fila_resumen = []
        list_encabezado = [
            'Cliente',
            'Documento',
            'Dirección',
            'Total Facturas',
            'Total Boletas',
            'Total Notas de Crédito',
            'Total',
            ]

        if count != 0:
            hoja = wb.create_sheet(str(departamento.nombre))
        else:
            hoja = wb.active
            hoja.title = str(departamento.nombre)

        hoja.append(tuple(list_encabezado))

        col_range = hoja.max_column  # get max columns in the worksheet
        # cabecera de la tabla
        for col in range(1, col_range + 1):
            cell_header = hoja.cell(1, col)
            cell_header.fill = RELLENO_EXCEL
            cell_header.font = NEGRITA
        
        total_total = Decimal('0.00')

        data = []
        
        for cliente in Cliente.objects.filter(distrito__provincia__departamento=departamento):
            total = Decimal('0.00')
            total_factura = Decimal('0.00')
            for factura in FacturaVenta.objects.filter(cliente=cliente, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin):
                if factura.moneda == moneda_base:
                    total_factura += factura.total
                else:
                    total_factura += (factura.total / factura.tipo_cambio).quantize(Decimal('0.01'))

            total_boleta = Decimal('0.00')
            for boleta in BoletaVenta.objects.filter(cliente=cliente, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin):
                if boleta.moneda == moneda_base:
                    total_boleta += boleta.total
                else:
                    total_boleta += (boleta.total / boleta.tipo_cambio).quantize(Decimal('0.01'))

            total_nota_credito = Decimal('0.00')
            for nota_credito in NotaCredito.objects.filter(cliente=cliente, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin):
                if nota_credito.moneda == moneda_base:
                    total_nota_credito += nota_credito.total
                else:
                    total_nota_credito += (nota_credito.total / nota_credito.tipo_cambio).quantize(Decimal('0.01'))

            total = total_factura + total_boleta - total_nota_credito
            total_total += total
            
            fila = []
            fila.append(cliente.razon_social)
            fila.append(f"{cliente.documento} - {cliente.numero_documento}")
            fila.append(cliente.direccion_fiscal)
            fila.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_factura))))
            fila.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_boleta))))
            fila.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_nota_credito))))
            fila.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(total))))
            data.append(fila)

        data.sort(key = lambda i: i[6], reverse=True) #Total
        
        for fila in data:
            hoja.append(fila)

        for row in hoja.rows:
            for col in range(hoja.max_column):
                row[col].border = BORDE_DELGADO
                if 3 <= col <= 6:
                    row[col].alignment = ALINEACION_DERECHA

        hoja.append(["","","","","","Total",("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_total))))])

        nueva_fila = hoja.max_row

        for col in range(1, col_range + 1):
            if col == 6:
                cell_header = hoja.cell(nueva_fila, col)
                cell_header.fill = RELLENO_EXCEL
                cell_header.font = NEGRITA
            elif col == 7:
                cell_header = hoja.cell(nueva_fila, col)
                cell_header.font = NEGRITA

        for i in range(hoja.max_row):
            if i >= nueva_fila-1:
                row = list(hoja.rows)[i]
                for col in range(hoja.max_column):
                    if col > 4:
                        row[col].border = BORDE_DELGADO
                        if col==5:
                            row[col].alignment = ALINEACION_CENTRO
                        elif col == 6:
                            row[col].alignment = ALINEACION_DERECHA


        total_resumen += total_total


        fila_resumen.append(departamento.nombre)
        fila_resumen.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_total))))
        fila_resumen.append(total_total)
        data_resumen.append(fila_resumen)

        hoja.freeze_panes = 'A2'
        ajustarColumnasSheet(hoja)
        count += 1

    list_encabezado_resumen = [
        'Departamento',
        'Total',
        'Porcentaje',
        ]
    hoja = wb.create_sheet('RESUMEN')
    
    hoja.append(tuple(list_encabezado_resumen))

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = RELLENO_EXCEL
        cell_header.font = NEGRITA
    
    data_resumen.sort(key = lambda i: i[2], reverse=True)

    for fila in data_resumen:
        fila[2] = ("%s %s" % (intcomma(redondear((Decimal(fila[2])/total_resumen)*100)), '%'))

    for fila in data_resumen:
        hoja.append(fila)

    for row in hoja.rows:
        for col in range(hoja.max_column):
            row[col].border = BORDE_DELGADO
            if col == 1 or col == 2:
                row[col].alignment = ALINEACION_DERECHA

    ajustarColumnasSheet(hoja)
    return wb

####################################################  CLIENTES CRM VS MEDIOS  ####################################################   

def dataClienteCRM():

    list_estado = ESTADOS_CLIENTE
    DICT_ESTADO = dict(list_estado)
    list_medio = MEDIO
    DICT_MEDIO = dict(list_medio)

    list_encabezado = [
        'Fecha de Registro',
        'Razón Social',
        'RUC',
        'País',
        'Distrito',
        'Fecha de Última Actividad',
        'Medio',
        'Estado',
        'Teléfono',
        'Correo Electrónico',
        ]

    wb = Workbook()
    hoja = wb.active
    hoja.title = 'Clientes'
    hoja.append(tuple(list_encabezado))

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = RELLENO_EXCEL
        cell_header.font = NEGRITA

    data = []
    
    for cliente in Cliente.objects.all():
        fila = []
        fila.append(cliente.created_at.strftime('%d/%m/%Y'))
        fila.append(cliente.razon_social)
        fila.append(cliente.numero_documento)
        fila.append(str(cliente.pais))
        fila.append(str(cliente.ubigeo_total))
        # cliente_crm_detalle = ClienteCRMDetalle.objects.filter(cliente_crm = cliente.id).order_by('-id')[0]
        # fila.append(cliente_crm_detalle.fecha.strftime('%d/%m/%Y'))
        # fila.append(DICT_MEDIO[cliente.medio])
        # fila.append(DICT_ESTADO[cliente.estado])
        fila.append("")
        fila.append("")
        fila.append("")
        try: 
            representante_legal = RepresentanteLegalCliente.objects.filter(cliente=cliente)[0]
            telefono =  TelefonoInterlocutorCliente.objects.filter(interlocutor=representante_legal.interlocutor)[0]
            fila.append(str(telefono.numero))
            correo = CorreoInterlocutorCliente.objects.filter(interlocutor=representante_legal.interlocutor)[0]
            fila.append(str(correo.correo))    

        except:
            fila.append("")
            fila.append("")
    
        data.append(fila)

    for fila in data:
        hoja.append(fila)

    for row in hoja.rows:
        for col in range(hoja.max_column):
            row[col].border = BORDE_DELGADO
            if col == 0 or col == 7:
                row[col].alignment = ALINEACION_CENTRO

    ajustarColumnasSheet(hoja)
    return wb

def ReporteClienteCRMExcel():

    wb=dataClienteCRM()
    return wb

####################################################  FACTURACIÓN GENERAL  ####################################################   

def dataFacturacionGeneral(fecha_inicio, fecha_fin):
    moneda_base = Moneda.objects.get(simbolo='$')

    list_encabezado = [
        'Razón Social',
        'Nro. Transacciones',
        'Monto Total',
        'Dias desde Registro',
        'Meses desde registro',
        'Años desde registro',
        'Correos Electrónicos',
        ]

    wb = Workbook()
    hoja = wb.active
    hoja.title = 'Facturación General'
    hoja.append(tuple(list_encabezado))

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = RELLENO_EXCEL
        cell_header.font = NEGRITA

    data = []
    for cliente in Cliente.objects.filter(estado_sunat = 1):
        total = Decimal('0.00')
        total_factura = Decimal('0.00')
        nf = 0
        nb = 0
        nn = 0
        for factura in FacturaVenta.objects.filter(cliente=cliente, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin.date()):
            if factura.moneda == moneda_base:
                total_factura += factura.total
            else:
                total_factura += (factura.total / factura.tipo_cambio).quantize(Decimal('0.01'))
            
            nf += 1

        total_boleta = Decimal('0.00')
        for boleta in BoletaVenta.objects.filter(cliente=cliente, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin.date()):
            if boleta.moneda == moneda_base:
                total_boleta += boleta.total
            else:
                total_boleta += (boleta.total / boleta.tipo_cambio).quantize(Decimal('0.01'))
            
            nb += 1

        total_nota_credito = Decimal('0.00')
        for nota_credito in NotaCredito.objects.filter(cliente=cliente, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin.date()):
            if nota_credito.moneda == moneda_base:
                total_nota_credito += nota_credito.total
            else:
                total_nota_credito += (nota_credito.total / nota_credito.tipo_cambio).quantize(Decimal('0.01'))
            
            nn += 1

        total = total_factura + total_boleta 
        total_transacciones = nf + nb 
        
        fila = []
        fila.append(cliente.razon_social)
        fila.append(total_transacciones)
        fila.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(total))))
        fecha_creacion = cliente.created_at.strftime('%Y-%m-%d')
        fecha_registro = datetime.strptime(fecha_creacion, '%Y-%m-%d')
        dias = (fecha_fin - fecha_registro) / timedelta(days=1)
        fila.append(dias)
        meses = (fecha_fin.year - fecha_registro.year)* 12 + (fecha_fin.month - fecha_registro.month)
        fila.append(meses)
        years = (fecha_fin.year - fecha_registro.year) + (fecha_fin.month - fecha_registro.month)/12
        fila.append(years)
        fila.append(cliente.correos)
        data.append(fila)

    for fila in data:
        hoja.append(fila)

    for row in hoja.rows:
        for col in range(hoja.max_column):
            row[col].border = BORDE_DELGADO
            if col == 1:
                row[col].alignment = ALINEACION_DERECHA
            elif col == 2:
                row[col].alignment = ALINEACION_DERECHA
                row[col].number_format = FORMATO_DOLAR
            elif 3 <= col <=5:
                row[col].alignment = ALINEACION_DERECHA
                row[col].number_format = FORMATO_NUMERO


    ajustarColumnasSheet(hoja)
    return wb
    
def ReporteFacturacionGeneral(fecha_inicio, fecha_fin):

    wb=dataFacturacionGeneral(fecha_inicio, fecha_fin)
    return wb

####################################################  COMPORTAMIENTO CLIENTE  ####################################################   

def dataComportamientoCliente(cliente):
    moneda_base = Moneda.objects.get(simbolo='$')

    list_encabezado = [
        'Razón Social',
        'Nro. Transacciones',
        'Monto Total',
        'Dias desde Registro',
        'Meses desde registro',
        'Años desde registro',
        'Correos Electrónicos',
        ]

    color_relleno = rellenoSociedad('None')

    wb = Workbook()
    hoja = wb.active
    hoja.title = "sheet"
    hoja.append(tuple(list_encabezado))

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = color_relleno
        cell_header.font = NEGRITA

    # data = []
    # for cliente in Cliente.objects.filter(estado_sunat = 1):
    #     total = Decimal('0.00')
    #     total_factura = Decimal('0.00')
    #     nf = 0
    #     nb = 0
    #     nn = 0
    #     for factura in FacturaVenta.objects.filter(cliente=cliente, estado=4, fecha_emision__lte=fecha_cierre.date()):
    #         if factura.moneda == moneda_base:
    #             total_factura += factura.total
    #         else:
    #             total_factura += (factura.total / factura.tipo_cambio).quantize(Decimal('0.01'))
            
    #         nf += 1

    #     total_boleta = Decimal('0.00')
    #     for boleta in BoletaVenta.objects.filter(cliente=cliente, estado=4, fecha_emision__lte=fecha_cierre.date()):
    #         if boleta.moneda == moneda_base:
    #             total_boleta += boleta.total
    #         else:
    #             total_boleta += (boleta.total / boleta.tipo_cambio).quantize(Decimal('0.01'))
            
    #         nb += 1

    #     total_nota_credito = Decimal('0.00')
    #     for nota_credito in NotaCredito.objects.filter(cliente=cliente, estado=4, fecha_emision__lte=fecha_cierre.date()):
    #         if nota_credito.moneda == moneda_base:
    #             total_nota_credito += nota_credito.total
    #         else:
    #             total_nota_credito += (nota_credito.total / nota_credito.tipo_cambio).quantize(Decimal('0.01'))
            
    #         nn += 1

    #     total = total_factura + total_boleta 
    #     total_transacciones = nf + nb 
        
    #     fila = []
    #     fila.append(cliente.razon_social)
    #     fila.append(total_transacciones)
    #     fila.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(total))))
    #     fecha_creacion = cliente.created_at.strftime('%Y-%m-%d')
    #     fecha_registro = datetime.strptime(fecha_creacion, '%Y-%m-%d')
    #     dias = (fecha_cierre - fecha_registro) / timedelta(days=1)
    #     fila.append(dias)
    #     meses = (fecha_cierre.year - fecha_registro.year)* 12 + (fecha_cierre.month - fecha_registro.month)
    #     fila.append(meses)
    #     years = (fecha_cierre.year - fecha_registro.year) + (fecha_cierre.month - fecha_registro.month)/12
    #     fila.append(years)
    #     fila.append(cliente.correos)
    #     data.append(fila)

    # for fila in data:
    #     hoja.append(fila)

    # for row in hoja.rows:
    #     for col in range(hoja.max_column):
    #         row[col].border = BORDE_DELGADO
    #         if col == 1:
    #             row[col].alignment = ALINEACION_DERECHA
    #         elif col == 2:
    #             row[col].alignment = ALINEACION_DERECHA
    #             row[col].number_format = FORMATO_DOLAR
    #         elif 3 <= col <=5:
    #             row[col].alignment = ALINEACION_DERECHA
    #             row[col].number_format = FORMATO_NUMERO


    ajustarColumnasSheet(hoja)
    return wb
    
def ReporteComportamientoCliente(cliente):

    wb=dataComportamientoCliente(cliente)
    return wb

####################################################  ESTADOS CLIENTE  ####################################################   

def dataEstadosCliente():

    list_estado = ESTADOS_CLIENTE
    DICT_ESTADO = dict(list_estado)
    list_medio = MEDIO
    DICT_MEDIO = dict(list_medio)

    list_encabezado = [
        'Fecha de Registro',
        'Razón Social',
        'RUC',
        'País',
        'Distrito',
        'Fecha de Última Actividad',
        'Medio',
        'Estado',
        'Teléfono',
        'Correo Electrónico',
        ]

    wb = Workbook()
    hoja = wb.active
    hoja.title = 'Clientes'
    hoja.append(tuple(list_encabezado))

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = RELLENO_EXCEL
        cell_header.font = NEGRITA

    data = []
    
    for cliente in Cliente.objects.all():
        fila = []
        fila.append(cliente.created_at.strftime('%d/%m/%Y'))
        fila.append(cliente.razon_social)
        fila.append(cliente.numero_documento)
        fila.append(str(cliente.pais))
        fila.append(str(cliente.ubigeo_total))
        # cliente_crm_detalle = ClienteCRMDetalle.objects.filter(cliente_crm = cliente.id).order_by('-id')[0]
        # fila.append(cliente_crm_detalle.fecha.strftime('%d/%m/%Y'))
        # fila.append(DICT_MEDIO[cliente.medio])
        # fila.append(DICT_ESTADO[cliente.estado])
        fila.append("")
        fila.append("")
        fila.append("")
        try: 
            representante_legal = RepresentanteLegalCliente.objects.filter(cliente=cliente)[0]
            telefono =  TelefonoInterlocutorCliente.objects.filter(interlocutor=representante_legal.interlocutor)[0]
            fila.append(str(telefono.numero))
            correo = CorreoInterlocutorCliente.objects.filter(interlocutor=representante_legal.interlocutor)[0]
            fila.append(str(correo.correo))    

        except:
            fila.append("")
            fila.append("")
    
        data.append(fila)

    for fila in data:
        hoja.append(fila)

    for row in hoja.rows:
        for col in range(hoja.max_column):
            row[col].border = BORDE_DELGADO
            if col == 0 or col == 7:
                row[col].alignment = ALINEACION_CENTRO

    ajustarColumnasSheet(hoja)
    return wb

def ReporteEstadosClienteExcel():

    wb=dataEstadosCliente()
    return wb

####################################################  REPORTE CONTADOR  ####################################################   

def dataReporteContador(sociedad, fecha_inicio, fecha_fin):
    moneda_base = Moneda.objects.get(simbolo='$')

    list_encabezado = [
        'FECHA',
        'TIPO DE COMP.',
        'N° COMPROB.',
        'RAZON SOCIAL',
        'RUC',
        'PRODUCTOS',
        'CANT.',
        'PRECIO UNIT. (US$) CON IGV',
        'MONTO (US$)',
        'IGV (US$)',
        'DESCUENTO GLOBAL',
        'TOTAL (US$)',
        'TIPO DE CAMBIO',
        'MONTO SOLES (S/)',
        'OBSERVACIONES',
        'LINK',
        ]

    wb = Workbook()
    hoja = wb.active
    hoja.title = 'Reporte'
    hoja.append(tuple(list_encabezado))

    color_relleno = rellenoSociedadCorregido(sociedad)

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = color_relleno
        cell_header.font = NEGRITA

    info = []
    facturas = FacturaVenta.objects.filter(
        fecha_emision__gte=fecha_inicio,
        fecha_emision__lte=fecha_fin,
        sociedad=sociedad,
    )
    boletas = BoletaVenta.objects.filter(
        fecha_emision__gte=fecha_inicio,
        fecha_emision__lte=fecha_fin,
        sociedad=sociedad,
    )

    tipo_cambio_sunat = TipoCambioSunat.objects.filter(
        fecha__gte=fecha_inicio,
        fecha__lte=fecha_fin,
    )

    for factura in facturas:
        tipo_cambio_sunat_documento = tipo_cambio_sunat.get(fecha=factura.fecha_emision)
        fila = []
        fila.append(factura.fecha_emision)  #0
        fila.append(factura.get_tipo_comprobante_display()) #1
        fila.append(f"{factura.serie_comprobante.serie}-{numeroXn(factura.numero_factura,6)}")    #2
        fila.append(factura.cliente.razon_social)   #3
        fila.append(factura.cliente.numero_documento)    #4
        contador = factura.contador
        fila.append(contador[0]) #5
        fila.append(contador[1])  #6
        fila.append(contador[2])  #7
        fila.append(factura.total_gravada)  #8
        fila.append(factura.total_igv)    #9
        fila.append(factura.descuento_global)   #10
        fila.append(factura.total)  #11
        fila.append(tipo_cambio_sunat_documento.tipo_cambio_venta.quantize(Decimal('0.01')))    #12
        fila.append(tipo_cambio_sunat_documento.tipo_cambio_venta * factura.total)    #13
        fila.append(factura.observaciones)  #14
        if factura.url_nubefact:
            fila.append(get_enlace_nubefact(factura.url_nubefact))   #15
        else:
            fila.append("")   #15
        fila.append(factura.estado) #16
        info.append(fila)

    for boleta in boletas:
        tipo_cambio_sunat_documento = tipo_cambio_sunat.get(fecha=boleta.fecha_emision)
        fila = []
        fila.append(boleta.fecha_emision)  #0
        fila.append(boleta.get_tipo_comprobante_display()) #1
        fila.append(f"{boleta.serie_comprobante.serie}-{numeroXn(boleta.numero_boleta,6)}")    #2
        fila.append(boleta.cliente.razon_social)   #3
        fila.append(boleta.cliente.numero_documento)    #4
        contador = boleta.contador
        fila.append(contador[0]) #5
        fila.append(contador[1])  #6
        fila.append(contador[2])  #7
        fila.append(boleta.total_gravada)  #8
        fila.append(boleta.total_igv)    #9
        fila.append(boleta.descuento_global)   #10
        fila.append(boleta.total)    #11
        fila.append(tipo_cambio_sunat_documento.tipo_cambio_venta.quantize(Decimal('0.01')))    #12
        fila.append(tipo_cambio_sunat_documento.tipo_cambio_venta * boleta.total)    #13
        fila.append(boleta.observaciones)  #14
        if boleta.url_nubefact:
            fila.append(get_enlace_nubefact(boleta.url_nubefact))   #15
        else:
            fila.append("")   #15
        fila.append(boleta.estado) #16
        info.append(fila)

    info.sort(key = lambda i:i[2])
    info.sort(key = lambda i:i[0])

    for fila in info:
        if fila[16] != 3:
            try:
                fila[8] = float(fila[8])
                fila[9] = float(fila[9])
                fila[10] =float(fila[10])
                fila[11] =float(fila[11])
                fila[12] = round(float(fila[12]),2)
                fila[13] = float(fila[13])
            except:
                pass
        else:
            for i in range(16):
                if i == 3:
                    fila[i] = 'ANULADO'
                elif i > 3:
                    fila[i] = ''
        fila.pop(-1)

    for fila in info:
        hoja.append(fila)

    for row in hoja.rows:
        for col in range(hoja.max_column):
            row[col].border = BORDE_DELGADO
            if 8 <= col <=11:
                row[col].alignment = ALINEACION_DERECHA
                row[col].number_format = FORMATO_DOLAR
            elif col == 13:
                row[col].alignment = ALINEACION_DERECHA
                row[col].number_format = FORMATO_SOLES
            elif col == 15:
                if row[col].value != 'LINK':
                    row[col].hyperlink =  row[col].value
                    row[col].font =  COLOR_AZUL

    info2 = []
    notas = NotaCredito.objects.filter(
        fecha_emision__gte=fecha_inicio,
        fecha_emision__lte=fecha_fin,
        sociedad=sociedad,
    )

    for nota in notas:
        fila = []
        fila.append(nota.fecha_emision) #0
        fila.append(nota.get_tipo_comprobante_display())    #1
        fila.append(f"{nota.serie_comprobante.serie}-{numeroXn(nota.numero_nota,6)}")    #2
        fila.append(nota.cliente.razon_social)  #3
        fila.append(nota.cliente.numero_documento)   #4
        fila.append(nota.documento.documento)  #5
        fila.append(nota.observaciones)   #6
        contador = nota.contador
        fila.append(contador[1])    #7
        fila.append(contador[0])    #8
        fila.append(contador[2])    #9
        fila.append(nota.descuento_global)  #10
        fila.append(nota.total_gravada)   #11
        fila.append(nota.total_igv)   #12
        fila.append(nota.total)   #13
        fila.append(nota.get_tipo_nota_credito_display())  #14
        if nota.url_nubefact:
            fila.append(get_enlace_nubefact(nota.url_nubefact))   #15
        else:
            fila.append("")   #15
        info2.append(fila)  

    for fila in info2:
        fila[10] = float(fila[10])
        fila[11] = float(fila[11])
        fila[12] = float(fila[12])
        fila[13] = float(fila[13])

    if info2 != []:
        # cabecera de la tabla
        hoja.append(('',)) # Crea la fila del encabezado con los títulos
        hoja.append(('FECHA', 'TIPO DE COMP.', 'N° COMPROB.', 'RAZON SOCIAL', 'RUC', 'COMPROBANTE QUE SE MODIFICA', '', 'CANT.', 'DESCRIPCION', 'PRECIO UNIT. (US$) SIN IGV', 'DESCUENTO GLOBAL', 'VALOR DE VENTA (US$)', 'IGV (US$)', 'TOTAL (US$)', 'MOTIVO DE LA NOTA', 'LINK')) # Crea la fila del encabezado con los títulos
        nueva_fila = hoja.max_row

        for col in range(1, col_range + 1):
            cell_header = hoja.cell(nueva_fila, col)
            cell_header.fill = color_relleno
            cell_header.font = NEGRITA

        for fila in info2:
            hoja.append(fila) # Crea la fila del encabezado con los títulos

        for i in range(hoja.max_row):
            if i >= nueva_fila-1:
                row = list(hoja.rows)[i]
                for col in range(hoja.max_column):
                    row[col].border = BORDE_DELGADO
                    if 10 <= col <=13:
                        row[col].alignment = ALINEACION_DERECHA
                        row[col].number_format = FORMATO_DOLAR
                    elif col == 15:
                        if row[col].value != 'LINK':
                            row[col].hyperlink =  row[col].value
                            row[col].font =  COLOR_AZUL

    ajustarColumnasSheet(hoja)
    return wb
    
def ReporteContadorCorregido(sociedad, fecha_inicio, fecha_fin):
    
    wb=dataReporteContador(sociedad, fecha_inicio, fecha_fin)
    return wb

####################################################  REPORTE ROTACIÓN  ####################################################   

def dataReporteRotacion2(sociedad=None):
    moneda_base = Moneda.objects.get(simbolo='$')

    list_encabezado = [
        'ID MAT.',
        'FAMILIA',
        'NOMBRE',
        'DESCRIPCIÓN',
        'PRECIO',
        'STOCK',
        'VENTA TOTAL',
        'VENTAS MENSUALES DEL TOTAL',
        'VENTA DESDE ÚLTIMOS 6 MESES (total/promedio)',
        'VENTA DESDE ULTIMO INGRESO (total/promedio)',
        'TIEMPO DURACION (APROX.)',
        'PEDIDO PARA 5 MESES',
        'SUGERENCIA',
        ]

    wb = Workbook()
    hoja = wb.active
    hoja.title = 'Reporte'
    hoja.append(tuple(list_encabezado))

    color_relleno = rellenoSociedadCorregido(sociedad)

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = color_relleno
        cell_header.font = NEGRITA

    lista_tipo_stock = [2,3,4,5,16,17,22,]
    # Recibido 2, Disponible 3, bloqueo sin serie 4, bloqueo sin qa 5, reservado 16, confirmado 17, prestado 22,
    # Recepcion compra 101, confirmacion por venta 120
    movimientos = MovimientosAlmacen.objects.filter(
        tipo_stock__codigo__in=lista_tipo_stock,
    )
    if sociedad:
        movimientos = movimientos.filter(
            sociedad=sociedad,
        )

    resumen = {}
    # id, familia, nombre, descripcion, precio, stock,
    # venta_total, fecha_inicial, fecha_final, venta_desde_6_meses, fecha_inicio_6_meses, venta_desde_ultimo_ingreso, fecha_ultimo_ingreso
    # tiempo_total = fecha_final - fecha_inicial
    # ventas_mensuales_del_total = 30 * venta_total / tiempo_total
    print("******************************************")
    print(len(movimientos), datetime.now())
    print("******************************************")
    for movimiento in movimientos:
        producto = movimiento.producto
        if producto == 'Error': continue
        if not producto in resumen:
            resumen[producto] = {
                'ID':producto.id,
                'FAMILIA':producto.subfamilia.familia.nombre,
                'NOMBRE':producto.descripcion_corta,
                'DESCRIPCION':producto.descripcion_venta,
                'PRECIO':producto.precio_lista,
                'FECHA INICIAL':None,
                'FECHA FINAL':None,
                'VENTA TOTAL':0,
                'FECHA INICIO 6 MESES':None,
                'VENTA 6 MESES':0,
                'FECHA ULTIMO INGRESO':None,
                'VENTA ULTIMO INGRESO':0,
                'INGRESOS':{},
                'VENTAS':{},
                'RECIBIDO':0,
                'DISPONIBLE':0,
                'BLOQUEO SIN SERIE':0,
                'BLOQUEO SIN QA':0,
                'RESERVADO':0,
                'CONFIRMADO':0,
                'PRESTADO':0,
            }
        if movimiento.tipo_movimiento.codigo == 101 and movimiento.tipo_stock.codigo == 2: #Recepción de compra : RECIBIDO
            if not resumen[producto]['FECHA ULTIMO INGRESO']:
                resumen[producto]['FECHA ULTIMO INGRESO'] = movimiento.fecha
            elif resumen[producto]['FECHA ULTIMO INGRESO'] < movimiento.fecha:
                resumen[producto]['FECHA ULTIMO INGRESO'] = movimiento.fecha
            if not movimiento.fecha in resumen[producto]['INGRESOS']: resumen[producto]['INGRESOS'][movimiento.fecha] = 0
            resumen[producto]['INGRESOS'][movimiento.fecha] = resumen[producto]['INGRESOS'][movimiento.fecha] + movimiento.cantidad
        elif movimiento.tipo_movimiento.codigo == 120 and movimiento.tipo_stock.codigo == 17: #Confirmado por venta : CONFIRMADO
            if not resumen[producto]['FECHA INICIAL']:
                resumen[producto]['FECHA INICIAL'] = movimiento.fecha
            elif resumen[producto]['FECHA INICIAL'] > movimiento.fecha:
                resumen[producto]['FECHA INICIAL'] = movimiento.fecha
            resumen[producto]['FECHA FINAL'] = movimiento.fecha
            if movimiento.fecha > date.today() - timedelta(180):
                resumen[producto]['VENTA 6 MESES'] = resumen[producto]['VENTA 6 MESES'] + movimiento.cantidad
                if not resumen[producto]['FECHA INICIO 6 MESES']:
                    resumen[producto]['FECHA INICIO 6 MESES'] = movimiento.fecha
                elif resumen[producto]['FECHA INICIO 6 MESES'] < movimiento.fecha:
                    resumen[producto]['FECHA INICIO 6 MESES'] = movimiento.fecha
            resumen[producto]['VENTA TOTAL'] = resumen[producto]['VENTA TOTAL'] + movimiento.cantidad
            if not movimiento.fecha in resumen[producto]['VENTAS']: resumen[producto]['VENTAS'][movimiento.fecha] = 0
            resumen[producto]['VENTAS'][movimiento.fecha] = resumen[producto]['VENTAS'][movimiento.fecha] + movimiento.cantidad

        if movimiento.tipo_stock.codigo == 2:
            resumen[producto]['RECIBIDO'] = resumen[producto]['RECIBIDO'] + movimiento.cantidad
        elif movimiento.tipo_stock.codigo == 3:
            resumen[producto]['DISPONIBLE'] = resumen[producto]['DISPONIBLE'] + movimiento.cantidad
        elif movimiento.tipo_stock.codigo == 4:
            resumen[producto]['BLOQUEO SIN SERIE'] = resumen[producto]['BLOQUEO SIN SERIE'] + movimiento.cantidad
        elif movimiento.tipo_stock.codigo == 5:
            resumen[producto]['BLOQUEO SIN QA'] = resumen[producto]['BLOQUEO SIN QA'] + movimiento.cantidad
        elif movimiento.tipo_stock.codigo == 16:
            resumen[producto]['RESERVADO'] = resumen[producto]['RESERVADO'] + movimiento.cantidad
        elif movimiento.tipo_stock.codigo == 17:
            resumen[producto]['CONFIRMADO'] = resumen[producto]['CONFIRMADO'] + movimiento.cantidad
        elif movimiento.tipo_stock.codigo == 22:
            resumen[producto]['PRESTADO'] = resumen[producto]['PRESTADO'] + movimiento.cantidad
            
    print("******************************************")
    print(len(resumen), datetime.now())
    print("******************************************")
    
    for producto, valores in resumen.items():
        fila = []
        precio_compra = Decimal('0.00')
        if valores['PRECIO']:
            precio_compra = valores['PRECIO'].precio_compra
        stock = valores['DISPONIBLE'] + valores['BLOQUEO SIN SERIE'] + valores['BLOQUEO SIN QA'] - valores['RESERVADO'] - valores['CONFIRMADO'] - valores['PRESTADO']
        if not valores['FECHA INICIAL'] and not valores['FECHA FINAL']:
            tiempo_total = None
        else:
            tiempo_total = (valores['FECHA FINAL'] - valores['FECHA INICIAL']).days
        if tiempo_total:
            ventas_mensuales = 30 * valores['VENTA TOTAL'] / tiempo_total
        else:
            ventas_mensuales = 30 * valores['VENTA TOTAL']

        if valores['FECHA INICIO 6 MESES']:
            tiempo_6_meses = (date.today() - valores['FECHA INICIO 6 MESES']).days
        else:
            tiempo_6_meses = 180
        if tiempo_6_meses:
            promedio_6_meses = 30 * valores['VENTA 6 MESES'] / tiempo_6_meses
        else:
            promedio_6_meses = 30 * valores['VENTA 6 MESES']

        for fecha, cantidad in valores['VENTAS'].items():
            if not valores['FECHA ULTIMO INGRESO']: valores['FECHA ULTIMO INGRESO'] = valores['FECHA INICIAL']
            if fecha >= valores['FECHA ULTIMO INGRESO']:
                valores['VENTA ULTIMO INGRESO'] = valores['VENTA ULTIMO INGRESO'] + cantidad
        
        tiempo_ultimo_ingreso = None
        if valores['FECHA ULTIMO INGRESO']:
            tiempo_ultimo_ingreso = (date.today() - valores['FECHA ULTIMO INGRESO']).days
        if tiempo_ultimo_ingreso:
            promedio_ultimo_ingreso = 30 * valores['VENTA ULTIMO INGRESO'] / tiempo_ultimo_ingreso
        else:
            promedio_ultimo_ingreso = 30 * valores['VENTA ULTIMO INGRESO']

        venta_promedio_mensual = Decimal(max(promedio_6_meses, promedio_ultimo_ingreso))

        if venta_promedio_mensual:
            tiempo_duracion = stock / venta_promedio_mensual
        else:
            tiempo_duracion = "-"

        pedido_5_meses = venta_promedio_mensual * 5

        if pedido_5_meses == 0:
            sugerencia = 'NO SE VENDIÓ'
        elif pedido_5_meses >= stock:
            sugerencia = 'EVALUAR'
        elif pedido_5_meses < stock:
            sugerencia = 'NO TRAER'

        fila.append(valores['ID'])
        fila.append(valores['FAMILIA'])
        fila.append(valores['NOMBRE'])
        fila.append(valores['DESCRIPCION'])
        fila.append(precio_compra)
        fila.append(stock)
        fila.append(valores['VENTA TOTAL'])
        fila.append(ventas_mensuales)
        fila.append(f"{valores['VENTA 6 MESES']} / {promedio_6_meses}")
        fila.append(f"{valores['VENTA ULTIMO INGRESO']} / {promedio_ultimo_ingreso}")
        fila.append(promedio_ultimo_ingreso)
        fila.append(tiempo_duracion)
        fila.append(pedido_5_meses)
        fila.append(sugerencia)
        
        hoja.append(fila)

    print("******************************************")
    print(datetime.now())
    print("******************************************")

    # for row in hoja.rows:
    #     for col in range(hoja.max_column):
    #         row[col].border = BORDE_DELGADO
    #         if 8 <= col <=11:
    #             row[col].alignment = ALINEACION_DERECHA
    #             row[col].number_format = FORMATO_DOLAR
    #         elif col == 13:
    #             row[col].alignment = ALINEACION_DERECHA
    #             row[col].number_format = FORMATO_SOLES
    #         elif col == 15:
    #             if row[col].value != 'LINK':
    #                 row[col].hyperlink =  row[col].value
    #                 row[col].font =  COLOR_AZUL

    ajustarColumnasSheet(hoja)
    return wb


def dataReporteRotacion(sociedad=None):
    moneda_base = Moneda.objects.get(simbolo='$')

    list_encabezado = [
        'ID MAT.',
        'FAMILIA',
        'NOMBRE',
        'DESCRIPCIÓN',
        'PRECIO',
        'STOCK',
        'VENTA TOTAL',
        'VENTAS MENSUALES DEL TOTAL',
        'VENTA DESDE ÚLTIMOS 6 MESES (total/promedio)',
        'VENTA DESDE ULTIMO INGRESO (total/promedio)',
        'TIEMPO DURACION (APROX.)',
        'PEDIDO PARA 5 MESES',
        'SUGERENCIA',
        ]

    wb = Workbook()
    hoja = wb.active
    hoja.title = 'Reporte'
    hoja.append(tuple(list_encabezado))

    color_relleno = rellenoSociedadCorregido(sociedad)

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = color_relleno
        cell_header.font = NEGRITA

    lista_tipo_stock = [2,3,4,5,16,17,22,]
    # Recibido 2, Disponible 3, bloqueo sin serie 4, bloqueo sin qa 5, reservado 16, confirmado 17, prestado 22,
    # Recepcion compra 101, confirmacion por venta 120
    materiales = Material.objects.filter(
            mostrar=True,
        ).annotate(
            familia_material=F('subfamilia__familia__nombre'),
        ).order_by('familia_material', 'descripcion_corta', 'descripcion_venta')
    
    stock = MovimientosAlmacen.objects.filter(
        content_type_producto=ContentType.objects.get_for_model(Material),
        tipo_stock__codigo__in=[3, 5, 36]
    ).values('id_registro_producto').annotate(
        stock=Sum(ExpressionWrapper(
            F('cantidad') * F('signo_factor_multiplicador'),
            output_field=FloatField()
        ))
    )

    pedidos = ComprobanteCompraPIDetalle.objects.filter(
        orden_compra_detalle__content_type_id=ContentType.objects.get_for_model(Material),
    ).values('orden_compra_detalle__id_registro').annotate(
        id_producto=F('orden_compra_detalle__id_registro'),
        precio_pedido=Sum('precio_final_con_igv'),
        fecha_pedido=Max('comprobante_compra__fecha_comprobante'),
    ).order_by('-comprobante_compra__fecha_comprobante')

    six_months_ago = datetime.now() - timedelta(days=180)

    rotacion_6ultimos_factura = FacturaVentaDetalle.objects.filter(
        content_type=ContentType.objects.get_for_model(Material),
        factura_venta__fecha_emision__gte=six_months_ago,
        factura_venta__estado='4'
    ).exclude(
        id_registro=None,
    ).values('id_registro').annotate(
        venta_6_meses=ExpressionWrapper(
            Sum('cantidad') / 6,
            output_field=FloatField()
        ),
    )
    
    rotacion_6ultimos_boleta = BoletaVentaDetalle.objects.filter(
        content_type=ContentType.objects.get_for_model(Material),
        boleta_venta__fecha_emision__gte=six_months_ago,
        boleta_venta__estado='4'
    ).exclude(
        id_registro=None,
    ).values('id_registro').annotate(
        venta_6_meses=ExpressionWrapper(
            Sum('cantidad') / 6,
            output_field=FloatField()
        ),
    )
    
    rotacion_factura = FacturaVentaDetalle.objects.filter(
        content_type=ContentType.objects.get_for_model(Material),
        factura_venta__estado='4',
    ).exclude(
        id_registro=None,
    ).values('id_registro').annotate(
        venta_total=Sum('cantidad'),
        venta_mensual=ExpressionWrapper(
            Sum('cantidad') / Case(
                When(created_at=F('factura_venta__created_at'), then=1),
                default=Sum('cantidad'),
                output_field=FloatField()
            ),
            output_field=FloatField()
        ),
    )
    
    rotacion_boleta = BoletaVentaDetalle.objects.filter(
        content_type=ContentType.objects.get_for_model(Material),
        boleta_venta__estado='4',
    ).exclude(
        id_registro=None,
    ).values('id_registro').annotate(
        venta_total=Sum('cantidad'),
        venta_mensual=ExpressionWrapper(
            Sum('cantidad') / Case(
                When(created_at=F('boleta_venta__created_at'), then=1),
                default=Sum('cantidad'),
                output_field=FloatField()
            ),
            output_field=FloatField()
        ),
    )

    venta_desde_ultimo_pedido_factura = FacturaVentaDetalle.objects.annotate(
        venta_desde_ultimo_pedido=ExpressionWrapper(
            Sum('cantidad') / Case(
                When(
                    created_at=F('factura_venta__created_at'),
                    then=1
                ),
                default=Sum('cantidad'),
                output_field=FloatField()
            ),
            output_field=FloatField()
        )
    ).filter(
        content_type=ContentType.objects.get_for_model(Material),
        created_at=F('factura_venta__created_at'),
        factura_venta__estado='4'
    ).values(
        'id_registro',
        'venta_desde_ultimo_pedido'
    )

    venta_desde_ultimo_pedido_boleta = BoletaVentaDetalle.objects.annotate(
        venta_desde_ultimo_pedido=ExpressionWrapper(
            Sum('cantidad') / Case(
                When(
                    created_at=F('boleta_venta__created_at'),
                    then=1
                ),
                default=Sum('cantidad'),
                output_field=FloatField()
            ),
            output_field=FloatField()
        )
    ).filter(
        content_type=ContentType.objects.get_for_model(Material),
        created_at=F('boleta_venta__created_at'),
        boleta_venta__estado='4'
    ).values(
        'id_registro',
        'venta_desde_ultimo_pedido'
    )

    
    print(materiales)
    print(stock)
    print(pedidos)
    print(rotacion_6ultimos_factura)
    print(rotacion_6ultimos_boleta)
    print(rotacion_factura)
    print(rotacion_boleta)
    print(venta_desde_ultimo_pedido_factura)
    print(venta_desde_ultimo_pedido_boleta)

    # resumen = {}
    # # id, familia, nombre, descripcion, precio, stock,
    # # venta_total, fecha_inicial, fecha_final, venta_desde_6_meses, fecha_inicio_6_meses, venta_desde_ultimo_ingreso, fecha_ultimo_ingreso
    # # tiempo_total = fecha_final - fecha_inicial
    # # ventas_mensuales_del_total = 30 * venta_total / tiempo_total
    # print("******************************************")
    # print(len(materiales), datetime.now())
    # print("******************************************")
    # for movimiento in movimientos:
    #     producto = movimiento.producto
    #     if producto == 'Error': continue
    #     if not producto in resumen:
    #         resumen[producto] = {
    #             'ID':producto.id,
    #             'FAMILIA':producto.subfamilia.familia.nombre,
    #             'NOMBRE':producto.descripcion_corta,
    #             'DESCRIPCION':producto.descripcion_venta,
    #             'PRECIO':producto.precio_lista,
    #             'FECHA INICIAL':None,
    #             'FECHA FINAL':None,
    #             'VENTA TOTAL':0,
    #             'FECHA INICIO 6 MESES':None,
    #             'VENTA 6 MESES':0,
    #             'FECHA ULTIMO INGRESO':None,
    #             'VENTA ULTIMO INGRESO':0,
    #             'INGRESOS':{},
    #             'VENTAS':{},
    #             'RECIBIDO':0,
    #             'DISPONIBLE':0,
    #             'BLOQUEO SIN SERIE':0,
    #             'BLOQUEO SIN QA':0,
    #             'RESERVADO':0,
    #             'CONFIRMADO':0,
    #             'PRESTADO':0,
    #         }
    #     if movimiento.tipo_movimiento.codigo == 101 and movimiento.tipo_stock.codigo == 2: #Recepción de compra : RECIBIDO
    #         if not resumen[producto]['FECHA ULTIMO INGRESO']:
    #             resumen[producto]['FECHA ULTIMO INGRESO'] = movimiento.fecha
    #         elif resumen[producto]['FECHA ULTIMO INGRESO'] < movimiento.fecha:
    #             resumen[producto]['FECHA ULTIMO INGRESO'] = movimiento.fecha
    #         if not movimiento.fecha in resumen[producto]['INGRESOS']: resumen[producto]['INGRESOS'][movimiento.fecha] = 0
    #         resumen[producto]['INGRESOS'][movimiento.fecha] = resumen[producto]['INGRESOS'][movimiento.fecha] + movimiento.cantidad
    #     elif movimiento.tipo_movimiento.codigo == 120 and movimiento.tipo_stock.codigo == 17: #Confirmado por venta : CONFIRMADO
    #         if not resumen[producto]['FECHA INICIAL']:
    #             resumen[producto]['FECHA INICIAL'] = movimiento.fecha
    #         elif resumen[producto]['FECHA INICIAL'] > movimiento.fecha:
    #             resumen[producto]['FECHA INICIAL'] = movimiento.fecha
    #         resumen[producto]['FECHA FINAL'] = movimiento.fecha
    #         if movimiento.fecha > date.today() - timedelta(180):
    #             resumen[producto]['VENTA 6 MESES'] = resumen[producto]['VENTA 6 MESES'] + movimiento.cantidad
    #             if not resumen[producto]['FECHA INICIO 6 MESES']:
    #                 resumen[producto]['FECHA INICIO 6 MESES'] = movimiento.fecha
    #             elif resumen[producto]['FECHA INICIO 6 MESES'] < movimiento.fecha:
    #                 resumen[producto]['FECHA INICIO 6 MESES'] = movimiento.fecha
    #         resumen[producto]['VENTA TOTAL'] = resumen[producto]['VENTA TOTAL'] + movimiento.cantidad
    #         if not movimiento.fecha in resumen[producto]['VENTAS']: resumen[producto]['VENTAS'][movimiento.fecha] = 0
    #         resumen[producto]['VENTAS'][movimiento.fecha] = resumen[producto]['VENTAS'][movimiento.fecha] + movimiento.cantidad

    #     if movimiento.tipo_stock.codigo == 2:
    #         resumen[producto]['RECIBIDO'] = resumen[producto]['RECIBIDO'] + movimiento.cantidad
    #     elif movimiento.tipo_stock.codigo == 3:
    #         resumen[producto]['DISPONIBLE'] = resumen[producto]['DISPONIBLE'] + movimiento.cantidad
    #     elif movimiento.tipo_stock.codigo == 4:
    #         resumen[producto]['BLOQUEO SIN SERIE'] = resumen[producto]['BLOQUEO SIN SERIE'] + movimiento.cantidad
    #     elif movimiento.tipo_stock.codigo == 5:
    #         resumen[producto]['BLOQUEO SIN QA'] = resumen[producto]['BLOQUEO SIN QA'] + movimiento.cantidad
    #     elif movimiento.tipo_stock.codigo == 16:
    #         resumen[producto]['RESERVADO'] = resumen[producto]['RESERVADO'] + movimiento.cantidad
    #     elif movimiento.tipo_stock.codigo == 17:
    #         resumen[producto]['CONFIRMADO'] = resumen[producto]['CONFIRMADO'] + movimiento.cantidad
    #     elif movimiento.tipo_stock.codigo == 22:
    #         resumen[producto]['PRESTADO'] = resumen[producto]['PRESTADO'] + movimiento.cantidad
            
    # print("******************************************")
    # print(len(resumen), datetime.now())
    # print("******************************************")
    
    # for producto, valores in resumen.items():
    #     fila = []
    #     precio_compra = Decimal('0.00')
    #     if valores['PRECIO']:
    #         precio_compra = valores['PRECIO'].precio_compra
    #     stock = valores['DISPONIBLE'] + valores['BLOQUEO SIN SERIE'] + valores['BLOQUEO SIN QA'] - valores['RESERVADO'] - valores['CONFIRMADO'] - valores['PRESTADO']
    #     if not valores['FECHA INICIAL'] and not valores['FECHA FINAL']:
    #         tiempo_total = None
    #     else:
    #         tiempo_total = (valores['FECHA FINAL'] - valores['FECHA INICIAL']).days
    #     if tiempo_total:
    #         ventas_mensuales = 30 * valores['VENTA TOTAL'] / tiempo_total
    #     else:
    #         ventas_mensuales = 30 * valores['VENTA TOTAL']

    #     if valores['FECHA INICIO 6 MESES']:
    #         tiempo_6_meses = (date.today() - valores['FECHA INICIO 6 MESES']).days
    #     else:
    #         tiempo_6_meses = 180
    #     if tiempo_6_meses:
    #         promedio_6_meses = 30 * valores['VENTA 6 MESES'] / tiempo_6_meses
    #     else:
    #         promedio_6_meses = 30 * valores['VENTA 6 MESES']

    #     for fecha, cantidad in valores['VENTAS'].items():
    #         if not valores['FECHA ULTIMO INGRESO']: valores['FECHA ULTIMO INGRESO'] = valores['FECHA INICIAL']
    #         if fecha >= valores['FECHA ULTIMO INGRESO']:
    #             valores['VENTA ULTIMO INGRESO'] = valores['VENTA ULTIMO INGRESO'] + cantidad
        
    #     tiempo_ultimo_ingreso = None
    #     if valores['FECHA ULTIMO INGRESO']:
    #         tiempo_ultimo_ingreso = (date.today() - valores['FECHA ULTIMO INGRESO']).days
    #     if tiempo_ultimo_ingreso:
    #         promedio_ultimo_ingreso = 30 * valores['VENTA ULTIMO INGRESO'] / tiempo_ultimo_ingreso
    #     else:
    #         promedio_ultimo_ingreso = 30 * valores['VENTA ULTIMO INGRESO']

    #     venta_promedio_mensual = Decimal(max(promedio_6_meses, promedio_ultimo_ingreso))

    #     if venta_promedio_mensual:
    #         tiempo_duracion = stock / venta_promedio_mensual
    #     else:
    #         tiempo_duracion = "-"

    #     pedido_5_meses = venta_promedio_mensual * 5

    #     if pedido_5_meses == 0:
    #         sugerencia = 'NO SE VENDIÓ'
    #     elif pedido_5_meses >= stock:
    #         sugerencia = 'EVALUAR'
    #     elif pedido_5_meses < stock:
    #         sugerencia = 'NO TRAER'

    #     fila.append(valores['ID'])
    #     fila.append(valores['FAMILIA'])
    #     fila.append(valores['NOMBRE'])
    #     fila.append(valores['DESCRIPCION'])
    #     fila.append(precio_compra)
    #     fila.append(stock)
    #     fila.append(valores['VENTA TOTAL'])
    #     fila.append(ventas_mensuales)
    #     fila.append(f"{valores['VENTA 6 MESES']} / {promedio_6_meses}")
    #     fila.append(f"{valores['VENTA ULTIMO INGRESO']} / {promedio_ultimo_ingreso}")
    #     fila.append(promedio_ultimo_ingreso)
    #     fila.append(tiempo_duracion)
    #     fila.append(pedido_5_meses)
    #     fila.append(sugerencia)
        
    #     hoja.append(fila)

    # print("******************************************")
    # print(datetime.now())
    # print("******************************************")

    # for row in hoja.rows:
    #     for col in range(hoja.max_column):
    #         row[col].border = BORDE_DELGADO
    #         if 8 <= col <=11:
    #             row[col].alignment = ALINEACION_DERECHA
    #             row[col].number_format = FORMATO_DOLAR
    #         elif col == 13:
    #             row[col].alignment = ALINEACION_DERECHA
    #             row[col].number_format = FORMATO_SOLES
    #         elif col == 15:
    #             if row[col].value != 'LINK':
    #                 row[col].hyperlink =  row[col].value
    #                 row[col].font =  COLOR_AZUL

    ajustarColumnasSheet(hoja)
    return wb
    
def ReporteRotacionCorregido(sociedad):
    
    wb=dataReporteRotacion(sociedad)
    return wb