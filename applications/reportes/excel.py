from django.shortcuts import render
import time
from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from applications.comprobante_compra.models import ComprobanteCompraPI, ComprobanteCompraPIDetalle
from applications.funciones import numeroXn
from applications.importaciones import *
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import PatternFill, Alignment
from openpyxl.styles import *
from openpyxl.styles.borders import Border, Side
from openpyxl.chart import Reference, Series,LineChart
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.plotarea import DataTable
from applications.material.models import Material
from applications.movimiento_almacen.managers import ordenar_movimientos
from applications.movimiento_almacen.models import MovimientosAlmacen
from applications.recepcion_compra.models import RecepcionCompra
from applications.reportes.funciones import *
from applications.datos_globales.models import CuentaBancariaSociedad, DocumentoFisico, Moneda, TipoCambioSunat
from applications.home.templatetags.funciones_propias import get_enlace_nubefact, redondear
from applications.comprobante_venta.models import BoletaVenta, BoletaVentaDetalle, FacturaVenta, FacturaVentaDetalle
from applications.nota.models import NotaCredito
from applications.crm.models import ClienteCRMDetalle
from applications.clientes.models import CorreoInterlocutorCliente, RepresentanteLegalCliente, TelefonoInterlocutorCliente
from applications.datos_globales.models import Departamento, Moneda
from applications.cotizacion.models import CotizacionVenta, PrecioListaMaterial
from applications.cobranza.models import Ingreso, Pago
from applications.reportes.data_resumen_ingresos_anterior import*

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
    movimientos = MovimientosAlmacen.objects.filter(
        tipo_stock__codigo__in=lista_tipo_stock,
        content_type_producto=ContentType.objects.get_for_model(Material),
    )
    if sociedad:
        movimientos = movimientos.filter(
            sociedad=sociedad,
        )

    # Obtén el último precio de lista para cada material
    ultimos_precios = PrecioListaMaterial.objects.filter(
        content_type_producto=ContentType.objects.get_for_model(Material),
        id_registro_producto=OuterRef('id')
    ).order_by('-created_at').values('precio_lista')[:1]


    # Consulta para obtener todos los materiales con subfamilia y último precio de lista
    materiales = Material.objects.annotate(
        precio=Subquery(ultimos_precios)
    )
    
    # FAMILIA.append(producto.subfamilia.familia.nombre)
    # NOMBRE.append(producto.descripcion_corta)
    # DESCRIPCION.append(producto.descripcion_venta)
    # PRECIO.append(producto.precio_lista)

    movimientos_valores = movimientos.values_list(
        'id_registro_producto',
        'fecha_documento',
        'tipo_movimiento__codigo',
        'tipo_stock__codigo',
        'cantidad',
        'signo_factor_multiplicador',
        )

    materiales_valores = materiales.values_list(
        'id',
        'subfamilia__familia__nombre',
        'descripcion_corta',
        'descripcion_venta',
        'precio',
        )
    
    # Convierte el diccionario en un DataFrame de Pandas
    dfMateriales = pd.DataFrame(materiales_valores, columns=['ID', 'FAMILIA', 'NOMBRE', 'DESCRIPCION', 'PRECIO'])
    df = pd.DataFrame(movimientos_valores, columns=['ID', 'FECHA', 'TIPO_MOVIMIENTO', 'TIPO_STOCK', 'CANTIDAD', 'FACTOR'])

    # Ahora df contiene los datos de la consulta ORM en un DataFrame de Pandas
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    
    # Suponiendo que tu DataFrame se llama df
    # Calcula la fecha actual
    fecha_actual = datetime.now()

    # Función personalizada para calcular STOCK
    def calcular_stock(group):
        filtro_stock = group['TIPO_STOCK'].isin([3, 4, 5]) & ~group['TIPO_STOCK'].isin([17, 22])
        return ((group.loc[filtro_stock, 'CANTIDAD'] * group.loc[filtro_stock, 'FACTOR']).sum() - 
                (group.loc[~filtro_stock, 'CANTIDAD'] * group.loc[~filtro_stock, 'FACTOR']).sum())

    # Función personalizada para calcular FECHA_VENTA_TOTAL
    def calcular_fecha_venta_total(group):
        filtro_venta_total = (group['TIPO_MOVIMIENTO'] == 120) & (group['TIPO_STOCK'] == 17)
        return (fecha_actual - group.loc[filtro_venta_total, 'FECHA'].min()).days

    # Función personalizada para calcular FECHA_ULTIMO_INGRESO
    def calcular_fecha_ultimo_ingreso(group):
        filtro_ultimo_ingreso = (group['TIPO_MOVIMIENTO'] == 101) & (group['TIPO_STOCK'] == 2)
        return (fecha_actual - group.loc[filtro_ultimo_ingreso, 'FECHA'].max()).days

    # Calcular la columna VENTA_ULTIMO_INGRESO para cada grupo
    def calcular_venta_ultimo_ingreso(group):
        ultimas_compras = group[(group['TIPO_MOVIMIENTO'] == 101) & (group['TIPO_STOCK'] == 2)]
        ultima_fecha_compra = ultimas_compras['FECHA'].max()
        group['VENTA_ULTIMO_INGRESO'] = group.apply(lambda row: row['CANTIDAD'] * row['FACTOR']
                                                    if row['TIPO_MOVIMIENTO'] == 120
                                                    and row['TIPO_STOCK'] == 17
                                                    and ultima_fecha_compra <= row['FECHA'] <= fecha_actual
                                                    else 0, axis=1)
        return group


    # Aplica las funciones personalizadas y agrupa por ID
    resultados = df.groupby('ID').apply(lambda group: pd.Series({
        'STOCK': calcular_stock(group),
        'FECHA_VENTA_TOTAL': calcular_fecha_venta_total(group),
        'VENTA_TOTAL': (group.loc[(group['TIPO_MOVIMIENTO'] == 120) & (group['TIPO_STOCK'] == 17), 'CANTIDAD'] * group.loc[(group['TIPO_MOVIMIENTO'] == 120) & (group['TIPO_STOCK'] == 17), 'FACTOR']).sum(),
        'VENTA_ULTIMOS_6_MESES': (group.loc[(group['TIPO_MOVIMIENTO'] == 120) & (group['TIPO_STOCK'] == 17) & (group['FECHA'] >= (fecha_actual - pd.Timedelta(days=180))), 'CANTIDAD'] * group.loc[(group['TIPO_MOVIMIENTO'] == 120) & (group['TIPO_STOCK'] == 17) & (group['FECHA'] >= (fecha_actual - pd.Timedelta(days=180))), 'FACTOR']).sum(),
        'FECHA_ULTIMO_INGRESO': calcular_fecha_ultimo_ingreso(group),
        'VENTA_ULTIMO_INGRESO': calcular_venta_ultimo_ingreso(group)
    }))
    resultados['STOCK'] = resultados['STOCK'].astype(float)
    resultados['FECHA_VENTA_TOTAL'] = resultados['FECHA_VENTA_TOTAL'].astype(float)
    resultados['VENTA_TOTAL'] = resultados['VENTA_TOTAL'].astype(float)
    resultados['VENTA_ULTIMOS_6_MESES'] = resultados['VENTA_ULTIMOS_6_MESES'].astype(float)
    resultados['FECHA_ULTIMO_INGRESO'] = resultados['FECHA_ULTIMO_INGRESO'].astype(float)

    # Calcula las demás columnas
    resultados['VENTA_MENSUALES_TOTAL'] = resultados['VENTA_TOTAL'] / resultados['FECHA_VENTA_TOTAL']
    resultados['VENTA_ULTIMOS_6_MESES_PROMEDIO'] = resultados['VENTA_ULTIMOS_6_MESES'] / 6
    resultados['VENTA_ULTIMO_INGRESO_PROMEDIO'] = (resultados['VENTA_TOTAL'] * 30) / resultados['FECHA_ULTIMO_INGRESO']
    resultados['TIEMPO_DURACION'] = resultados['STOCK'] / resultados[['VENTA_MENSUALES_TOTAL', 'VENTA_ULTIMOS_6_MESES_PROMEDIO', 'VENTA_ULTIMO_INGRESO_PROMEDIO']].max(axis=1)
    resultados['PEDIDO_5_MESES'] = 5 * resultados[['VENTA_MENSUALES_TOTAL', 'VENTA_ULTIMOS_6_MESES_PROMEDIO', 'VENTA_ULTIMO_INGRESO_PROMEDIO']].max(axis=1)
    resultados['SUGERENCIA'] = 'NO SE VENDIÓ'
    resultados.loc[resultados['PEDIDO_5_MESES'] >= resultados['STOCK'], 'SUGERENCIA'] = 'EVALUAR'
    resultados.loc[resultados['PEDIDO_5_MESES'] < resultados['STOCK'], 'SUGERENCIA'] = 'EVALUAR'

    # Ver los resultados
    resultados.reset_index(inplace=True)
    print(resultados)

    resultado_combinado = pd.merge(dfMateriales, resultados, on='ID', how='right')

    
    for r_idx, row in enumerate(dataframe_to_rows(resultado_combinado, index=False, header=True), 2):
        # if r_idx == 1: continue
        print(row)
        hoja.cell(row=r_idx, column=1, value=row[0])
        hoja.cell(row=r_idx, column=2, value=row[1])
        hoja.cell(row=r_idx, column=3, value=row[2])
        hoja.cell(row=r_idx, column=4, value=row[3])
        hoja.cell(row=r_idx, column=5, value=row[4])
        hoja.cell(row=r_idx, column=6, value=row[5])

        hoja.cell(row=r_idx, column=7, value=row[7])
        hoja.cell(row=r_idx, column=8, value=row[7])
        hoja.cell(row=r_idx, column=9, value=row[8])
        hoja.cell(row=r_idx, column=10, value=row[9])
        hoja.cell(row=r_idx, column=11, value=row[10])
        hoja.cell(row=r_idx, column=12, value=row[11])
        hoja.cell(row=r_idx, column=13, value=row[12])

        hoja.cell(row=r_idx, column=14, value=row[13])
        hoja.cell(row=r_idx, column=15, value=row[14])
        hoja.cell(row=r_idx, column=16, value=row[15])
        
        
        # for c_idx, value in enumerate(row, 1):
        #     hoja.cell(row=r_idx, column=c_idx, value=value)

    # # Aplicar formato a las columnas específicas
    # venta_total_column = hoja['C']
    # venta_total_column.font = Font(bold=True)

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

####################################################  REPORTE DEPÓSITOS CUENTAS BANCARIAS  ####################################################   


def dataReporteDepositoCuentasBancarias(sociedad, fecha_inicio, fecha_fin):
    moneda_dolar = Moneda.objects.get(simbolo='$')
    moneda_sol = Moneda.objects.get(simbolo='S/')

    wb = Workbook()
    hoja = wb.active
    color_relleno = rellenoSociedadCorregido(sociedad)

    cuentas = CuentaBancariaSociedad.objects.filter(
        sociedad = sociedad, 
        estado = 1, 
        efectivo = False
        )
    
    info_cuentas = []
    for cuenta in cuentas:
        data = []
        if cuenta.banco:
            data.append(cuenta.banco.razon_social)
            data.append(cuenta.sociedad.razon_social)
            data.append(cuenta.numero_cuenta)
            data.append(cuenta.numero_cuenta_interbancaria)
            data.append(cuenta.moneda.nombre)
            info_cuentas.append(data)

    tipo_cambio_sunat = TipoCambioSunat.objects.filter(
        fecha__gte=fecha_inicio,
        fecha__lte=fecha_fin,
        )

    list_temp_hojas = []
    dict_totales_cuentas = {}
    count_cuenta = 0
    list_nro_cuentas = []
    for fila in info_cuentas:
        nro_cuenta = fila[2]
        list_nro_cuentas.append("%s %s" %(fila[0],fila[4]))
        info_depositos = []
        # numero_operacion = []

        ################################## Version N° 1 ##################################

        ingresos = Ingreso.objects.filter(
            cuenta_bancaria__numero_cuenta = nro_cuenta, 
            cuenta_bancaria__estado = 1, 
            cuenta_bancaria__efectivo = False, 
            fecha__gte=fecha_inicio, 
            fecha__lte=fecha_fin,).order_by('fecha')

        for ingreso in ingresos:
            if ingreso.pagos:
                data = []
                tipo_cambio_sunat_documento = tipo_cambio_sunat.get(fecha=ingreso.fecha)
                data.append(ingreso.fecha.strftime('%d/%m/%Y'))
                data.append(ingreso.numero_operacion)
                if ingreso.cuenta_bancaria.moneda.abreviatura == "USD":
                    data.append(ingreso.monto)
                    data.append(ingreso.monto*tipo_cambio_sunat_documento.tipo_cambio_venta)
                else:
                    data.append(ingreso.monto/tipo_cambio_sunat_documento.tipo_cambio_venta)
                    data.append(ingreso.monto)
                for pago in ingreso.pagos:
                    if pago == ingreso.pagos[0]:
                        data.append(pago.deuda.documento_objeto[3].razon_social)
                        data.append("%s: %s" % (pago.deuda.documento_objeto[0], pago.deuda.documento_objeto[1]))
                        data.append(pago.deuda.documento_objeto[2].strftime('%d/%m/%Y'))
                        if ingreso.cuenta_bancaria.moneda.abreviatura == "USD":
                            data.append("%s %s" %(moneda_dolar.simbolo, intcomma(redondear(pago.monto))))
                            data.append("%s %s" %(moneda_sol.simbolo, intcomma(redondear(pago.monto*tipo_cambio_sunat_documento.tipo_cambio_venta))))
                        else:
                            data.append("%s %s" %(moneda_dolar.simbolo, intcomma(redondear(pago.monto/tipo_cambio_sunat_documento.tipo_cambio_venta))))
                            data.append("%s %s" %(moneda_sol.simbolo, intcomma(redondear(pago.monto))))
                    else:
                        data[4] = "%s\n%s" %(data[4], pago.deuda.documento_objeto[3].razon_social)
                        data[5] = "%s\n%s" %(data[5], "%s: %s" % (pago.deuda.documento_objeto[0], pago.deuda.documento_objeto[1]))
                        data[6] = "%s\n%s" %(data[6], pago.deuda.documento_objeto[2].strftime('%d/%m/%Y'))
                        if ingreso.cuenta_bancaria.moneda.abreviatura == "USD":
                            data[7] = "%s\n%s" %(data[7], "%s %s" %(moneda_dolar.simbolo, intcomma(redondear(pago.monto))))
                            data[8] = "%s\n%s" %(data[8], "%s %s" %(moneda_sol.simbolo, intcomma(redondear(pago.monto*tipo_cambio_sunat_documento.tipo_cambio_venta))))
                        else:
                            data[7] = "%s\n%s" %(data[7], "%s %s" %(moneda_dolar.simbolo, intcomma(redondear(pago.monto/tipo_cambio_sunat_documento.tipo_cambio_venta))))
                            data[8] = "%s\n%s" %(data[8], "%s %s" %(moneda_sol.simbolo, intcomma(redondear(pago.monto)))) 
                info_depositos.append(data)

            else:
                data = []
                tipo_cambio_sunat_documento = tipo_cambio_sunat.get(fecha=ingreso.fecha)
                data.append(ingreso.fecha.strftime('%d/%m/%Y'))
                if ingreso.comentario:
                    data.append("%s | %s" % (ingreso.numero_operacion, ingreso.comentario))
                else:
                    data.append("%s | %s" % (ingreso.numero_operacion, 'Sin Comentario'))
                if ingreso.cuenta_bancaria.moneda.abreviatura == "USD":
                    data.append(ingreso.monto)
                    data.append(ingreso.monto*tipo_cambio_sunat_documento.tipo_cambio_venta)
                else:
                    data.append(ingreso.monto/tipo_cambio_sunat_documento.tipo_cambio_venta)
                    data.append(ingreso.monto)
                
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                data.append('')
                info_depositos.append(data)
        
        ################################## Version N° 2 ##################################

        # depositos = Pago.objects.filter(
        #     content_type = ContentType.objects.get_for_model(Ingreso),
        #     id_registro__in = [ingreso.id for ingreso in Ingreso.objects.filter(
        #         cuenta_bancaria__numero_cuenta = nro_cuenta, 
        #         cuenta_bancaria__estado = 1, 
        #         cuenta_bancaria__efectivo = False, 
        #         fecha__gte=fecha_inicio, 
        #         fecha__lte=fecha_fin,).order_by('fecha')],
        #         )
        
        # for deposito in depositos:
        #     num_operacion = "%s,%s" %(deposito.ingreso_nota.fecha, deposito.ingreso_nota.numero_operacion)
        #     if num_operacion in numero_operacion:
        #         pos = numero_operacion.index(num_operacion)
        #         info_depositos[pos][4] = "%s\n%s" %(info_depositos[pos][4], deposito.deuda.documento_objeto[3].razon_social)
        #         info_depositos[pos][5] = "%s\n%s" %(info_depositos[pos][5], "%s: %s" % (deposito.deuda.documento_objeto[0], deposito.deuda.documento_objeto[1]))
        #         info_depositos[pos][6] = "%s\n%s" %(info_depositos[pos][6], deposito.deuda.documento_objeto[2].strftime('%d/%m/%Y'))
        #         if deposito.ingreso_nota.cuenta_bancaria.moneda.abreviatura == "USD":
        #             info_depositos[pos][7] = "%s\n%s" %(info_depositos[pos][7], "%s %s" %(moneda_dolar.simbolo, intcomma(redondear(deposito.monto))))
        #             info_depositos[pos][8] = "%s\n%s" %(info_depositos[pos][8], "%s %s" %(moneda_sol.simbolo, intcomma(redondear(deposito.monto*tipo_cambio_sunat_documento.tipo_cambio_venta))))
        #         else:
        #             info_depositos[pos][7] = "%s\n%s" %(info_depositos[pos][7], "%s %s" %(moneda_dolar.simbolo, intcomma(redondear(deposito.monto/tipo_cambio_sunat_documento.tipo_cambio_venta))))
        #             info_depositos[pos][8] = "%s\n%s" %(info_depositos[pos][8], "%s %s" %(moneda_sol.simbolo, intcomma(redondear(deposito.monto))))                  

        #     else:
        #         data = []
        #         numero_operacion.append(num_operacion)
        #         tipo_cambio_sunat_documento = tipo_cambio_sunat.get(fecha=deposito.ingreso_nota.fecha)
        #         data.append(deposito.ingreso_nota.fecha.strftime('%d/%m/%Y'))
        #         data.append(deposito.ingreso_nota.numero_operacion)
        #         if deposito.ingreso_nota.cuenta_bancaria.moneda.abreviatura == "USD":
        #             data.append(deposito.ingreso_nota.monto)
        #             data.append(deposito.ingreso_nota.monto*tipo_cambio_sunat_documento.tipo_cambio_venta)
        #         else:
        #             data.append(deposito.ingreso_nota.monto/tipo_cambio_sunat_documento.tipo_cambio_venta)
        #             data.append(deposito.ingreso_nota.monto)
        #         data.append(deposito.deuda.documento_objeto[3].razon_social)
        #         data.append("%s: %s" % (deposito.deuda.documento_objeto[0], deposito.deuda.documento_objeto[1]))
        #         data.append(deposito.deuda.documento_objeto[2].strftime('%d/%m/%Y'))
        #         if deposito.ingreso_nota.cuenta_bancaria.moneda.abreviatura == "USD":
        #             data.append("%s %s" %(moneda_dolar.simbolo, intcomma(redondear(deposito.monto))))
        #             data.append("%s %s" %(moneda_sol.simbolo, intcomma(redondear(deposito.monto*tipo_cambio_sunat_documento.tipo_cambio_venta))))
        #         else:
        #             data.append("%s %s" %(moneda_dolar.simbolo, intcomma(redondear(deposito.monto/tipo_cambio_sunat_documento.tipo_cambio_venta))))
        #             data.append("%s %s" %(moneda_sol.simbolo, intcomma(redondear(deposito.monto))))
        #         info_depositos.append(data)

        # ingresos = Ingreso.objects.filter(
        #     cuenta_bancaria__numero_cuenta = nro_cuenta, 
        #     cuenta_bancaria__estado = 1, 
        #     cuenta_bancaria__efectivo = False, 
        #     fecha__gte=fecha_inicio, 
        #     fecha__lte=fecha_fin,
        #     es_pago=False,
        #     pendiente_usar=True,).order_by('fecha')

        # for ingreso in ingresos:
        #     num_operacion = "%s,%s" %(ingreso.fecha, ingreso.numero_operacion)
        #     if num_operacion not in numero_operacion:
        #         data = []
        #         tipo_cambio_sunat_documento = tipo_cambio_sunat.get(fecha=ingreso.fecha)
        #         data.append(ingreso.fecha.strftime('%d/%m/%Y'))
        #         if ingreso.comentario:
        #             data.append("%s | %s" % (ingreso.numero_operacion, ingreso.comentario))
        #         else:
        #             data.append("%s | %s" % (ingreso.numero_operacion, 'Sin Comentario'))
        #         if ingreso.cuenta_bancaria.moneda.abreviatura == "USD":
        #             data.append(ingreso.monto)
        #             data.append(ingreso.monto*tipo_cambio_sunat_documento.tipo_cambio_venta)
        #         else:
        #             data.append(ingreso.monto/tipo_cambio_sunat_documento.tipo_cambio_venta)
        #             data.append(ingreso.monto)
                
        #         data.append('')
        #         data.append('')
        #         data.append('')
        #         data.append('')
        #         data.append('')
        #         info_depositos.append(data)

        # info_depositos.sort(key = lambda i: datetime.strptime(i[0], '%d/%m/%Y'), reverse=False)

        count_cuenta += 1
        # print('**********************************')
        # print(info_depositos)
        # print('**********************************')
        count_mes = 0
        list_general = []
        list_mes = []
        for deposito in info_depositos:
            if count_mes != 0:
                año_mes_actual = deposito[0][6:] + deposito[0][3:5]
                año_mes_anterior = info_depositos[count_mes-1][0][6:] + info_depositos[count_mes-1][0][3:5]
                if año_mes_actual != año_mes_anterior:
                    list_general.append(list_mes)
                    list_mes = []
            list_mes.append(deposito)
            try:
                deposito[2] = float(deposito[2])
                deposito[3] = float(deposito[3])
            except:
                ""
            count_mes += 1
        if list_mes != []:
            list_general.append(list_mes)
        # print('**********************************')
        # print(list_general)
        # print('**********************************')

        count = 0
        for list_mes_deposito in list_general:
            mes = list_mes_deposito[0][0][3:5]
            año = list_mes_deposito[0][0][6:]
            name_sheet = DICT_MESES[str(mes)] + ' - ' + str(año)
            # print('*************************************')
            # print(str(mes), name_sheet, list_temp_hojas)
            # print('*************************************')
            if count != 0:
                if name_sheet not in list_temp_hojas:
                    hoja = wb.create_sheet(name_sheet)
                    list_temp_hojas.append(name_sheet)
                else:
                    hoja = wb[name_sheet]
            else:
                hoja = wb.active
                hoja.title = name_sheet
                if name_sheet not in list_temp_hojas:
                    list_temp_hojas.append(name_sheet)
                count += 1
                # count_cuenta += 1

            hoja.append(('', ''))
            hoja.append(('', ''))
            hoja.append(('BANCO:', fila[0]))
            hoja.append(('EMPRESA:', fila[1]))
            hoja.append(('CUENTA:', fila[2]))
            hoja.append(('CCI:', fila[3]))
            hoja.append(('MONEDA:', fila[4]))
            # wb.active = hoja
            hoja.append(('FECHA', 'REFERENCIA', 'MONTO (US$)', 'MONTO (S/)', 'EMPRESAS', 'DOCUMENTOS', 'FECHA DOCUMENTOS', 'PAGOS (US$)', 'PAGOS (S/)'))
            col_range = hoja.max_column
            nueva_fila = hoja.max_row

            for col in range(1, col_range + 1):
                cell_header = hoja.cell(nueva_fila, col)
                cell_header.fill = color_relleno
                cell_header.font = NEGRITA
                for count_fila in range(1,6):
                    cell_header = hoja.cell(nueva_fila-count_fila, col)
                    cell_header.fill = color_relleno

            total_mes_cuenta_dolares = 0
            total_mes_cuenta_soles = 0
            for fila_deposito in list_mes_deposito:
                if fila_deposito[4] != "" and fila_deposito[4] != None:
                    if 'Nota Credito:' not in fila_deposito[1]:
                        total_mes_cuenta_dolares += float(fila_deposito[2])
                        try:
                            total_mes_cuenta_soles += float(fila_deposito[3])
                        except:
                            pass
                hoja.append(fila_deposito)
            cuenta_banco_ingreso = fila[0] + ' ' + fila[4]
            dict_totales_cuentas[cuenta_banco_ingreso + '|' + name_sheet] = str(round(total_mes_cuenta_soles,2)) + '|' + str(round(total_mes_cuenta_dolares,2))

            for i in range(hoja.max_row):
                if i >= nueva_fila-1:
                    row = list(hoja.rows)[i]
                    for col in range(hoja.max_column):
                        row[col].border = BORDE_DELGADO
                        if col == 2:
                            row[col].alignment = ALINEACION_DERECHA
                            row[col].number_format = FORMATO_DOLAR
                        if col == 3:
                            row[col].alignment = ALINEACION_DERECHA
                            row[col].number_format = FORMATO_SOLES
                        if 4 <= col <= 6:
                            row[col].alignment = AJUSTAR_TEXTO
                        if col == 7 or col == 8:
                            row[col].alignment = AJUSTAR_TEXTO_DERECHA

            ajustarColumnasSheet(hoja)

    hoja = wb.create_sheet('Resumen Ingresos')
    # hoja.append(('', ''))
    hoja.append(('ENERO', 'FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SETIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'))
    hoja.append(('', ''))
    num_cuentas = len(list_nro_cuentas)
    hoja.cell(row= 3, column=1).value = "SOLES"
    hoja.cell(row= 3, column= num_cuentas+4).value = "DÓLARES"
    hoja.merge_cells(start_row = 3, start_column = 1, end_row = 3, end_column = num_cuentas+2)
    hoja.merge_cells(start_row = 3, start_column = num_cuentas+4, end_row = 3, end_column = 2*num_cuentas+5)
    celda_multiple = hoja.cell(row = 3, column = 1)
    celda_multiple.alignment = ALINEACION_CENTRO
    celda_multiple = hoja.cell(row = 3, column = num_cuentas+4)
    celda_multiple.alignment = ALINEACION_CENTRO
    list_encabezado = [''] + list_nro_cuentas + ['TOTAL','',''] + list_nro_cuentas + ['TOTAL']
    hoja.append(tuple(list_encabezado))

    col_range = 2*num_cuentas+5
    nueva_fila = hoja.max_row
    for col in range(1, col_range+1):
        if col != num_cuentas+3:
            cell_header = hoja.cell(nueva_fila, col)
            cell_header.fill = color_relleno
            cell_header.font = NEGRITA
            for count_fila in range(1,2):
                cell_header = hoja.cell(nueva_fila-count_fila, col)
                cell_header.fill = color_relleno

    def insertarResumenDataAnterior(hoja, data):
        for fila in data:
            hoja.append(fila)
        # return hoja
        
    if str(fecha_inicio) <= '2022-01-01':
        if sociedad.id == 2:
            insertarResumenDataAnterior(hoja, list_resumen_ingresos_sis_anterior_mpl)
        if sociedad.id == 1:
            insertarResumenDataAnterior(hoja, list_resumen_ingresos_sis_anterior_mca)

    for mes in list_temp_hojas:
        list_temp_fila = []
        # list_temp.append(mes)
        list_temp_soles = []
        list_temp_dolares = []
        total_soles = 0
        total_dolares = 0
        for k,value in dict_totales_cuentas.items():
            if mes in k:
                # print(k)
                monto_soles = float(value[:value.find("|")])
                monto_dolares = float(value[value.find("|")+1:])
                total_soles += monto_soles
                total_dolares += monto_dolares
                list_temp_soles.append(monto_soles)
                list_temp_dolares.append(monto_dolares)
                
        if len(list_temp_soles) < num_cuentas:
            while len(list_temp_soles) == num_cuentas:
                list_temp_soles.insert(len(list_temp_soles), " ")
                list_temp_dolares.insert(len(list_temp_dolares), " ")

        list_temp_soles.append(total_soles)
        list_temp_dolares.append(total_dolares)
        list_temp_fila = [mes] + list_temp_soles + ['', mes] + list_temp_dolares
        hoja.append(tuple(list_temp_fila))

    i = 0
    for row in hoja.rows:
        if i >= 2:
            for col in range(col_range):
                if col != num_cuentas+2:
                    row[col].border = BORDE_DELGADO
                if 1 <= col <= num_cuentas + 1:
                    row[col].number_format = FORMATO_SOLES
                if col >= num_cuentas + 4:
                    row[col].number_format = FORMATO_DOLAR
        i += 1
    ajustarColumnasSheet(hoja)

    def extraer_resumen_bloc_de_notas(hoja):

        # nro_col = col_range
        file_mpl = open(f'resumen_ingresos_{sociedad.abreviatura}_{fecha_inicio}_{fecha_fin}.txt', "w")
        file = file_mpl

        list_temp = []
        for i in range(5, hoja.max_row + 1): # Nro de filas del excel
            celda = hoja.cell(row = i, column = col_range)
            if celda.value == None:
                valor_celda = ''
            else:
                valor_celda = celda.value
            list_temp.append(valor_celda)
        # print(list_temp)

        for pos in range(len(list_temp)):
            list_temp[pos] = str(round(list_temp[pos],2))

        info = '\n'.join(list_temp)
        file.write(info)
        file.close()

    extraer_resumen_bloc_de_notas(hoja)

    def grafico_resumen_ingresos(ws):
        max_fila = ws.max_row

        chart = LineChart()
        # print(help(chart))
        chart.height = 15 # default is 7.5
        chart.width = 30 # default is 15
        chart.y_axis.title = 'INGRESOS'
        chart.x_axis.title = 'MESES'
        chart.legend.position = 'b' #bottom
        # chart.style = 12

        count = 1
        fila_base = 5
        year_base = 2018
        chart.title = f'RESUMEN DE INGRESOS - {sociedad.abreviatura}'
        data_col = col_range # montos en dolares

        while max_fila >= 12:
            values = Reference(ws, min_col = data_col, min_row = fila_base + 12*(count-1), max_col = data_col, max_row = 12*count + fila_base - 1)
            series = Series(values, title = "Ingresos del " + str(year_base + count))
            chart.append(series)
            max_fila -= 12
            count += 1
        if 1 <= max_fila <= 12:
            values = Reference(ws, min_col = data_col, min_row = fila_base + 12*(count-1), max_col = data_col, max_row = 12*count + fila_base - 1)
            series = Series(values, title = "Ingresos del " + str(year_base + count))
            chart.append(series)

        meses = Reference(ws, min_col = 1, min_row = 1, max_col = 12, max_row = 1)
        chart.set_categories(meses)
        chart.dataLabels = DataLabelList()
        chart.dataLabels.showVal = True
        chart.dataLabels.dLblPos = 't' # top

        chart.plot_area.dTable = DataTable()
        chart.plot_area.dTable.showHorzBorder = True
        chart.plot_area.dTable.showVertBorder = True
        chart.plot_area.dTable.showOutline = True
        chart.plot_area.dTable.showKeys = True

        ws.add_chart(chart)

    grafico_resumen_ingresos(hoja)

    return wb

def dataReporteDepositoCuentasBancariasResumen(sociedades,fecha_inicio, fecha_fin):
    nombres_soc = []
    listas = []
    for sociedad in sociedades:
        try:
            file = open(f'resumen_ingresos_{sociedad.abreviatura}_{fecha_inicio}_{fecha_fin}.txt', "r")
            contenido = file.read()
            file.close()
            lista = contenido.split("\n")
            for pos in range(len(lista)):
                if lista[pos] != "":
                    lista[pos]=float(lista[pos])
                else:
                    lista[pos]=float('0.00')
            listas.append(lista)
            nombres_soc.append(sociedad.nombre_comercial)
        except Exception as e:
            print(e)
            

    max_lon = max(list(map(len, listas)))
    rango_listas = range(len(listas))
    rango_max = range(max_lon)
    
    listas_todas_empresas = []

    for b in rango_max:
        total_lista = float('0.00')
        for a in rango_listas:
            if b in range(len(listas[a])):
                total_lista+=listas[a][b]
            else:
                total_lista+=float('0.00')

        listas_todas_empresas.append(total_lista)

    wb = Workbook()
    hoja = wb.active
    hoja.append(('','ENERO', 'FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SETIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'))
    # for dato in list_ambas_empresas:
    for dato in listas_todas_empresas:
        hoja.append((dato,''))

    for row in hoja.rows:
        for col in range(hoja.max_column):
            row[col].border = BORDE_DELGADO
            if col == 0:
                row[col].number_format = FORMATO_DOLAR

    def grafico_resumen_ingresos(ws):
        max_fila = ws.max_row

        chart = LineChart()
        # print(help(chart))
        chart.height = 15 # default is 7.5
        chart.width = 30 # default is 15
        chart.y_axis.title = 'INGRESOS'
        chart.x_axis.title = 'MESES'
        chart.legend.position = 'b' #bottom
        chart.title = f'RESUMEN DE INGRESOS - {" + ".join(nombres_soc)}'
        # chart.style = 12

        count = 1
        fila_base = 2
        year_base = 2018
        data_col = 1 # montos en dolares
        while max_fila >= 12:
            values = Reference(ws, min_col = data_col, min_row = fila_base + 12*(count-1), max_col = data_col, max_row = 12*count + fila_base - 1)
            series = Series(values, title = "Ingresos del " + str(year_base + count))
            chart.append(series)
            max_fila -= 12
            count += 1
        if 1 <= max_fila <= 12:
            values = Reference(ws, min_col = data_col, min_row = fila_base + 12*(count-1), max_col = data_col, max_row = 12*count + fila_base - 1)
            series = Series(values, title = "Ingresos del " + str(year_base + count))
            chart.append(series)

        meses = Reference(ws, min_col = 2, min_row = 1, max_col = 13, max_row = 1)
        chart.set_categories(meses)
        chart.dataLabels = DataLabelList()
        chart.dataLabels.showVal = True
        chart.dataLabels.dLblPos = 't' # top

        chart.plot_area.dTable = DataTable()
        chart.plot_area.dTable.showHorzBorder = True
        chart.plot_area.dTable.showVertBorder = True
        chart.plot_area.dTable.showOutline = True
        chart.plot_area.dTable.showKeys = True

        ws.add_chart(chart)

    grafico_resumen_ingresos(hoja)

    return wb
    
def ReporteDepositoCuentasBancariasCorregido(sociedad_id, fecha_inicio, fecha_fin):

    if sociedad_id:
        sociedad = Sociedad.objects.get(id=sociedad_id)
        wb=dataReporteDepositoCuentasBancarias(sociedad, fecha_inicio, fecha_fin)
        return wb
    else:
        sociedades = Sociedad.objects.all()
        wb=dataReporteDepositoCuentasBancariasResumen(sociedades, fecha_inicio, fecha_fin)
        return wb
