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
from applications.datos_globales.models import Moneda
from applications.home.templatetags.funciones_propias import redondear
from applications.comprobante_venta.models import BoletaVenta, FacturaVenta
from applications.nota.models import NotaCredito
from applications.crm.models import ClienteCRM, ClienteCRMDetalle
from applications.clientes.models import CorreoInterlocutorCliente, RepresentanteLegalCliente, TelefonoInterlocutorCliente
from applications.datos_globales.models import Departamento, Moneda

####################################################  FACTURACIÓN VS ASESOR COMERCIAL  ####################################################   

def dataReporteFacturacionAsesorComercial(wb, count,fecha_inicio, fecha_fin, asesor_comercial):
    moneda_base = Moneda.objects.get(simbolo='$')

    list_encabezado = [
        'Usuario',
        'Fecha Emisión',
        'N° Comprobante',
        'Total',

        ]
    
    color_relleno = rellenoSociedad('None')
    if count != 0:
        hoja = wb.create_sheet(str(asesor_comercial.username))
        # wb.active = hoja
    else:
        hoja = wb.active
        hoja.title = str(asesor_comercial.username)
        count += 1
    # hoja = wb.active
    # hoja.title = str(asesor_comercial.username)
    hoja.append(tuple(list_encabezado))

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = color_relleno
        cell_header.font = NEGRITA

    # total_total = Decimal('0.00')
    data = []
    
    # for asesor in get_user_model().objects.filter(is_active=1, id=asesor_comercial):
    total = Decimal('0.00')
    total_factura = Decimal('0.00')
    for factura in FacturaVenta.objects.filter(created_by_id=asesor_comercial.id, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin):
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
        fila.append(f"{str(factura.serie_comprobante.serie)} - {str(factura.numero_factura).zfill(6)}")
        fila.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(factura.total))))
        data.append(fila)


    total_boleta = Decimal('0.00')
    for boleta in BoletaVenta.objects.filter(created_by=asesor_comercial, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin):
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
        fila.append(f"{str(boleta.serie_comprobante.serie)} - {str(boleta.numero_boleta).zfill(6)}")
        fila.append("%s %s" % (moneda_base.simbolo, intcomma(redondear(boleta.total))))
        data.append(fila)

        # total_nota_credito = Decimal('0.00')
        # for nota_credito in NotaCredito.objects.filter(created_by=asesor_comercial, estado=4, fecha_emision__gte=fecha_inicio, fecha_emision__lte=fecha_fin):
        #     if nota_credito.moneda == moneda_base:
        #         total_nota_credito += nota_credito.total
        #     else:
        #         total_nota_credito += (nota_credito.total / nota_credito.tipo_cambio).quantize(Decimal('0.01'))

        # total = total_factura + total_boleta - total_nota_credito
    total = total_factura + total_boleta
        # total_total += total
        

    data.sort(key = lambda i: i[1], reverse=False)
    data.append(["","","TOTAL",("%s %s" % (moneda_base.simbolo, intcomma(redondear(total))))])

    for fila in data:
        hoja.append(fila)

    for row in hoja.rows:
        for col in range(hoja.max_column):
            row[col].border = BORDE_DELGADO
            if col == 1 or col==2:
                row[col].alignment = ALINEACION_CENTRO
            elif col == 3:
                row[col].alignment = ALINEACION_DERECHA

    ajustarColumnasSheet(hoja)
    return wb

def ReporteFacturacionAsesorComercial(fecha_inicio, fecha_fin, asesor_comercial):

    if asesor_comercial:
        asesores = get_user_model().objects.filter(id=asesor_comercial)
    else:
        asesores = get_user_model().objects.filter(is_active=1)

    wb = Workbook()
    count = 0
    for asesor_comercial in asesores:
        wb = dataReporteFacturacionAsesorComercial(wb, count, fecha_inicio, fecha_fin, asesor_comercial)
        count += 1
    
    return wb

####################################################  VENTAS VS DEPARTAMENTO  ####################################################   

def dataReporteVentasDepartamento(wb, count, titulo, fecha_inicio, fecha_fin, departamento):
    moneda_base = Moneda.objects.get(simbolo='$')


    list_encabezado = [
        'Cliente',
        'Documento',
        'Dirección',
        'Total Facturas',
        'Total Boletas',
        'Total Notas de Crédito',
        'Total',
        ]
    
    color_relleno = rellenoSociedad('None')
    if count != 0:
        hoja = wb.create_sheet(str(departamento.nombre))
        # wb.active = hoja
    else:
        hoja = wb.active
        hoja.title = str(departamento.nombre)
        count += 1
    # hoja = wb.active
    # hoja.title = str(asesor_comercial.username)
    hoja.append(tuple(list_encabezado))

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = color_relleno
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
    
    data.append(["","","","","","Total",("%s %s" % (moneda_base.simbolo, intcomma(redondear(total_total))))])

    for fila in data:
        hoja.append(fila)

    for row in hoja.rows:
        for col in range(hoja.max_column):
            row[col].border = BORDE_DELGADO
            if 3 <= col <= 6:
                row[col].alignment = ALINEACION_DERECHA

    ajustarColumnasSheet(hoja)
    return wb

def ReporteVentasDepartamento(titulo, fecha_inicio, fecha_fin, departamento_codigo):

    if departamento_codigo:
        departamentos = Departamento.objects.filter(codigo=departamento_codigo)
    else:
        departamentos = Departamento.objects.all()

    wb = Workbook()
    count = 0
    for departamento in departamentos:
        wb = dataReporteVentasDepartamento(wb, count, titulo, fecha_inicio, fecha_fin, departamento)
        count += 1

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

    color_relleno = rellenoSociedad('None')

    wb = Workbook()
    hoja = wb.active
    hoja.title = 'Cliente CRM'
    hoja.append(tuple(list_encabezado))

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = color_relleno
        cell_header.font = NEGRITA

    data = []
    
    for cliente in ClienteCRM.objects.all():
        fila = []
        fila.append(cliente.cliente_crm.created_at.strftime('%d/%m/%Y'))
        fila.append(cliente.cliente_crm.razon_social)
        fila.append(cliente.cliente_crm.numero_documento)
        fila.append(str(cliente.cliente_crm.pais))
        fila.append(str(cliente.cliente_crm.ubigeo_total))
        cliente_crm_detalle = ClienteCRMDetalle.objects.filter(cliente_crm = cliente.id).order_by('-id')[0]
        fila.append(cliente_crm_detalle.fecha.strftime('%d/%m/%Y'))
        fila.append(DICT_MEDIO[cliente.medio])
        fila.append(DICT_ESTADO[cliente.estado])
        try: 
            representante_legal = RepresentanteLegalCliente.objects.filter(cliente=cliente.cliente_crm)[0]
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

def dataFacturacionGeneral(fecha_cierre):
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
    hoja.title = 'Facturación General'
    hoja.append(tuple(list_encabezado))

    col_range = hoja.max_column  # get max columns in the worksheet
    # cabecera de la tabla
    for col in range(1, col_range + 1):
        cell_header = hoja.cell(1, col)
        cell_header.fill = color_relleno
        cell_header.font = NEGRITA

    data = []
    for cliente in Cliente.objects.filter(estado_sunat = 1):
        total = Decimal('0.00')
        total_factura = Decimal('0.00')
        nf = 0
        nb = 0
        nn = 0
        for factura in FacturaVenta.objects.filter(cliente=cliente, estado=4, fecha_emision__lte=fecha_cierre.date()):
            if factura.moneda == moneda_base:
                total_factura += factura.total
            else:
                total_factura += (factura.total / factura.tipo_cambio).quantize(Decimal('0.01'))
            
            nf += 1

        total_boleta = Decimal('0.00')
        for boleta in BoletaVenta.objects.filter(cliente=cliente, estado=4, fecha_emision__lte=fecha_cierre.date()):
            if boleta.moneda == moneda_base:
                total_boleta += boleta.total
            else:
                total_boleta += (boleta.total / boleta.tipo_cambio).quantize(Decimal('0.01'))
            
            nb += 1

        total_nota_credito = Decimal('0.00')
        for nota_credito in NotaCredito.objects.filter(cliente=cliente, estado=4, fecha_emision__lte=fecha_cierre.date()):
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
        dias = (fecha_cierre - fecha_registro) / timedelta(days=1)
        fila.append(dias)
        meses = (fecha_cierre.year - fecha_registro.year)* 12 + (fecha_cierre.month - fecha_registro.month)
        fila.append(meses)
        years = (fecha_cierre.year - fecha_registro.year) + (fecha_cierre.month - fecha_registro.month)/12
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
    
def ReporteFacturacionGeneral(fecha_cierre):

    wb=dataFacturacionGeneral(fecha_cierre)
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