from django.shortcuts import render
import time
from datetime import datetime, timedelta
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType
from applications.importaciones import *
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Alignment
from openpyxl.styles import *
from openpyxl.styles.borders import Border, Side
from openpyxl.chart import Reference, Series,LineChart
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.plotarea import DataTable
from applications.reportes.funciones import *
from applications.datos_globales.models import DocumentoFisico, Moneda
from applications.home.templatetags.funciones_propias import redondear
from applications.comprobante_venta.models import BoletaVenta, FacturaVenta
from applications.nota.models import NotaCredito
from applications.crm.models import ClienteCRM, ClienteCRMDetalle
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

    list_estado = ESTADOS_CLIENTE_CRM
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

    list_estado = ESTADOS_CLIENTE_CRM
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
