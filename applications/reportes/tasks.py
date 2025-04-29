# # tasks.py
# from openpyxl import Workbook
# from openpyxl.styles import PatternFill, Alignment
# from openpyxl.styles import *
# from openpyxl.styles.borders import Border, Side
# from openpyxl.chart import Reference, Series,LineChart
# from openpyxl.chart.label import DataLabelList
# from openpyxl.chart.plotarea import DataTable

# from background_task import background
# from applications.comprobante_venta.models import FacturaVenta
# from applications.nota.models import NotaCredito

# from applications.reportes.funciones import *
# from django.http import HttpResponse

# def consultaNotasContador(global_sociedad, global_fecha_inicio, global_fecha_fin):
#     sql = ''' (SELECT
#         MAX(nnc.id) AS id,
#         to_char(MAX(nnc.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_nota,
#         (CASE WHEN nnc.tipo_comprobante='3' THEN 'NOTA DE CRÉDITO' ELSE '-' END) as comprobante,
#         CONCAT(MAX(dgsc.serie), '-', lpad(CAST(nnc.numero_nota AS TEXT), 6, '0')) as nro_comprobante,
#         MAX(cc.razon_social) AS cliente_denominacion,
#         MAX(cc.numero_documento) AS ruc,
#         CONCAT(MAX(dgsc2.serie), '-', MAX(lpad(CAST(cvf.numero_factura AS TEXT), 6, '0'))) AS comprobante_modifica,
#         '' AS obs,
#         STRING_AGG(CAST(ROUND(nncd.cantidad, 2) AS TEXT), ' | ') AS cantidad,
#         STRING_AGG(mm.descripcion_corta, ' | ') AS productos,
#         STRING_AGG(CAST(ROUND(nncd.precio_unitario_sin_igv, 2) AS TEXT), ' | ') AS precios,
#         MAX(nnc.descuento_global) AS dscto_global,
#         ROUND(SUM(nncd.sub_total), 2) AS valor_venta,
#         SUM(nncd.igv)AS igv,
#         ROUND(SUM(nncd.total), 2) AS total_venta,
#         MAX(nnc.tipo_nota_credito) AS motivo_nota,
#         MAX(nnc.nubefact) AS url_nota
#         FROM nota_notacredito nnc
#         LEFT JOIN datos_globales_seriescomprobante dgsc
#             ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=nnc.serie_comprobante_id AND dgsc.id='10'
#         LEFT JOIN clientes_cliente cc
#             ON cc.id=nnc.cliente_id
#         LEFT JOIN datos_globales_documentofisico dgdf
#             ON dgdf.id=nnc.content_type_documento_id AND dgdf.modelo_id='%s'
#         LEFT JOIN comprobante_venta_facturaventa cvf
#             ON cvf.id=nnc.id_registro_documento
#         LEFT JOIN datos_globales_seriescomprobante dgsc2
#             ON dgsc2.tipo_comprobante_id='%s' AND dgsc2.id=cvf.serie_comprobante_id
#         LEFT JOIN nota_notacreditodetalle nncd
#             ON nnc.id=nncd.nota_credito_id
#         LEFT JOIN material_material mm
#             ON nncd.content_type_id='%s' AND mm.id=nncd.id_registro
#         WHERE dgsc.serie!='' AND nnc.sociedad_id='%s' AND '%s' <= nnc.fecha_emision AND nnc.fecha_emision <= '%s'
#         GROUP BY nnc.sociedad_id, nnc.tipo_comprobante, nnc.serie_comprobante_id, nnc.numero_nota) 
#         UNION
#         (SELECT
#         MAX(nnc.id) AS id,
#         to_char(MAX(nnc.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_nota,
#         (CASE WHEN nnc.tipo_comprobante='3' THEN 'NOTA DE CRÉDITO' ELSE '-' END) as comprobante,
#         CONCAT(MAX(dgsc.serie), '-', lpad(CAST(nnc.numero_nota AS TEXT), 6, '0')) as nro_comprobante,
#         MAX(cc.razon_social) AS cliente_denominacion,
#         MAX(cc.numero_documento) AS ruc,
#         CONCAT(MAX(dgsc2.serie), '-', MAX(lpad(CAST(cvb.numero_boleta AS TEXT), 6, '0'))) AS comprobante_modifica,
#         '' AS obs,
#         STRING_AGG(CAST(ROUND(nncd.cantidad, 2) AS TEXT), ' | ') AS cantidad,
#         STRING_AGG(mm.descripcion_corta, ' | ') AS productos,
#         STRING_AGG(CAST(ROUND(nncd.precio_unitario_sin_igv, 2) AS TEXT), ' | ') AS precios,
#         MAX(nnc.descuento_global) AS dscto_global,
#         ROUND(SUM(nncd.sub_total), 2) AS valor_venta,
#         SUM(nncd.igv)AS igv,
#         ROUND(SUM(nncd.total), 2) AS total_venta,
#         MAX(nnc.tipo_nota_credito) AS motivo_nota,
#         MAX(nnc.nubefact) AS url_nota
#         FROM nota_notacredito nnc
#         LEFT JOIN datos_globales_seriescomprobante dgsc
#             ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=nnc.serie_comprobante_id AND dgsc.id='11'
#         LEFT JOIN clientes_cliente cc
#             ON cc.id=nnc.cliente_id
#         LEFT JOIN datos_globales_documentofisico dgdf
#             ON dgdf.id=nnc.content_type_documento_id AND dgdf.modelo_id='%s'
#         LEFT JOIN comprobante_venta_boletaventa cvb
#             ON cvb.id=nnc.id_registro_documento
#         LEFT JOIN datos_globales_seriescomprobante dgsc2
#             ON dgsc2.tipo_comprobante_id='%s' AND dgsc2.id=cvb.serie_comprobante_id
#         LEFT JOIN nota_notacreditodetalle nncd
#             ON nnc.id=nncd.nota_credito_id
#         LEFT JOIN material_material mm
#             ON nncd.content_type_id='%s' AND mm.id=nncd.id_registro
#         WHERE dgsc.serie!='' AND nnc.sociedad_id='%s' AND '%s' <= nnc.fecha_emision AND nnc.fecha_emision <= '%s'
#         GROUP BY nnc.sociedad_id, nnc.tipo_comprobante, nnc.serie_comprobante_id, nnc.numero_nota) 
#         ORDER BY fecha_emision_nota, nro_comprobante ;''' %(DICT_CONTENT_TYPE['nota | notacredito'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['material | material'], global_sociedad,global_fecha_inicio, global_fecha_fin, DICT_CONTENT_TYPE['nota | notacredito'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['material | material'], global_sociedad,global_fecha_inicio, global_fecha_fin)
#     query_info = NotaCredito.objects.raw(sql)
    
#     info = []
#     for fila in query_info:
#         lista_datos = []
#         lista_datos.append(fila.fecha_emision_nota)
#         lista_datos.append(fila.comprobante)
#         lista_datos.append(fila.nro_comprobante)
#         lista_datos.append(fila.cliente_denominacion)
#         lista_datos.append(fila.ruc)
#         lista_datos.append(fila.comprobante_modifica)
#         lista_datos.append(fila.obs)
#         lista_datos.append(fila.cantidad)
#         lista_datos.append(fila.productos)
#         lista_datos.append(fila.precios)
#         lista_datos.append(fila.dscto_global)
#         lista_datos.append(fila.valor_venta)
#         lista_datos.append(fila.igv)
#         lista_datos.append(fila.total_venta)
#         lista_datos.append(str(fila.motivo_nota))
#         lista_datos.append(fila.url_nota)
#         info.append(lista_datos)

#     for fila in info:
#         fila[10] =float(fila[10])
#         fila[11] =float(fila[11])
#         fila[12] = float(fila[12])
#         fila[13] = float(fila[13])
#         fila[14] = DICT_TIPO_NOTA_CREDITO[fila[14]]
#     return info

# def consultaFacturasContador(global_sociedad, global_fecha_inicio, global_fecha_fin):
#     # global_fecha_inicio = '2022-01-01'
#     # global_fecha_fin = '2022-01-31'

#     sql_anuladas = ''' (SELECT
#         MAX(cvf.id) as id,
#         CONCAT(MAX(dgsc.serie), '-', MAX(lpad(CAST(cvf.numero_factura AS TEXT), 6, '0'))) as nro_comprobante
#         FROM comprobante_venta_facturaventa cvf
#         LEFT JOIN datos_globales_seriescomprobante dgsc
#             ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
#         WHERE cvf.estado='3' and cvf.sociedad_id='%s'
#         GROUP BY cvf.sociedad_id, cvf.serie_comprobante_id, cvf.numero_factura)
#         UNION
#         (SELECT
#         MAX(cvb.id) as id,
#         CONCAT(MAX(dgsc.serie), '-', MAX(lpad(CAST(cvb.numero_boleta AS TEXT), 6, '0'))) as nro_comprobante
#         FROM comprobante_venta_boletaventa cvb
#         LEFT JOIN datos_globales_seriescomprobante dgsc
#             ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
#         WHERE cvb.estado='3' and cvb.sociedad_id='%s'
#         GROUP BY cvb.sociedad_id, cvb.serie_comprobante_id, cvb.numero_boleta) ; ''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], global_sociedad, DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], global_sociedad)
#     query_info_anulados = FacturaVenta.objects.raw(sql_anuladas)

#     info_anulados = []
#     for fila in query_info_anulados:
#         list_temp = []
#         list_temp.append(fila.nro_comprobante)
#         info_anulados.append(list_temp)  

#     # print('****************************')
#     # print(info_anulados)
#     # print('****************************')

#     list_anulados = []
#     for fact in info_anulados:
#         list_anulados.append(fact[0])

#     sql = ''' (SELECT
#         MAX(cvf.id) AS id,
#         MAX(cvf.fecha_emision) AS fecha_orden,
#         to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
#         'FACTURA' AS tipo_comprobante,
#         CONCAT(MAX(dgsc.serie), '-', MAX(lpad(CAST(cvf.numero_factura AS TEXT), 6, '0'))) AS nro_comprobante,
#         MAX(cc.razon_social) AS cliente_denominacion,
#         MAX(cc.numero_documento) AS ruc,
#         STRING_AGG(mm.descripcion_corta, ' | ') AS productos,
#         STRING_AGG(CAST(ROUND(cvfd.cantidad, 2) AS TEXT), ' | ') AS cantidad,
#         STRING_AGG(CAST(ROUND(cvfd.precio_final_con_igv, 2) AS TEXT), ' | ') AS precio_final,
#         ROUND((SUM(cvfd.total)-ROUND((MAX(cvf.descuento_global)*1.18),2))/1.18,2) AS monto,
#         MAX(cvf.total_igv) AS igv,
#         MAX(cvf.descuento_global) AS dscto_global,
#         SUM(cvfd.total)-ROUND((MAX(cvf.descuento_global)*1.18),2) AS total_dolares,
#         ROUND(MAX(dgtc.tipo_cambio_venta), 2) AS tipo_cambio_fact,
#         ROUND((SUM(cvfd.total)-ROUND((MAX(cvf.descuento_global)*1.18),2))*MAX(dgtc.tipo_cambio_venta),2) AS total_soles,
#         '' AS observaciones,
#         (CASE WHEN MAX(cvf.nubefact) IS NOT NULL THEN MAX(cvf.nubefact) ELSE MAX(dgnr.respuesta->>'enlace') END) AS link_nubefact
#         FROM comprobante_venta_facturaventa cvf
#         LEFT JOIN datos_globales_seriescomprobante dgsc
#             ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
#         LEFT JOIN clientes_cliente cc
#             ON cc.id=cvf.cliente_id
#         LEFT JOIN comprobante_venta_facturaventadetalle cvfd
#             ON cvf.id=cvfd.factura_venta_id
#         LEFT JOIN material_material mm
#             ON cvfd.content_type_id='%s' AND mm.id=cvfd.id_registro
#         LEFT JOIN datos_globales_tipocambiosunat dgtc
#             ON dgtc.fecha=cvf.fecha_emision
#         LEFT JOIN datos_globales_nubefactrespuesta dgnr
#             ON dgnr.content_type_id='%s' AND dgnr.id_registro=cvf.id AND dgnr.error=False AND dgnr.id=(select max(id) from datos_globales_nubefactrespuesta  where content_type_id='%s' AND id_registro=dgnr.id_registro AND dgnr.error=False)
#         WHERE cvf.sociedad_id='%s' AND '%s' <= cvf.fecha_emision AND cvf.fecha_emision <= '%s'
#         GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura)
#         UNION
#         (SELECT
#         MAX(cvb.id) as id,
#         MAX(cvb.fecha_emision) AS fecha_orden,
#         to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
#         'BOLETA' AS tipo_comprobante,
#         CONCAT(MAX(dgsc.serie), '-', MAX(lpad(CAST(cvb.numero_boleta AS TEXT), 6, '0'))) as nro_comprobante,
#         MAX(cc.razon_social) AS cliente_denominacion,
#         MAX(cc.numero_documento) AS ruc,
#         STRING_AGG(mm.descripcion_corta, ' | ') AS productos,
#         STRING_AGG(CAST(ROUND(cvbd.cantidad, 2) AS TEXT), ' | ') AS cantidad,
#         STRING_AGG(CAST(ROUND(cvbd.precio_final_con_igv, 2) AS TEXT), ' | ') AS precio_final,
#         ROUND((SUM(cvbd.total)-ROUND((MAX(cvb.descuento_global)*1.18),2))/1.18,2) AS monto,
#         MAX(cvb.total_igv) AS igv,
#         MAX(cvb.descuento_global) AS dscto_global,
#         SUM(cvbd.total)-ROUND((MAX(cvb.descuento_global)*1.18),2) AS total_dolares,
#         ROUND(MAX(dgtc.tipo_cambio_venta), 2) AS tipo_cambio_fact,
#         ROUND((SUM(cvbd.total)-ROUND((MAX(cvb.descuento_global)*1.18),2))*MAX(dgtc.tipo_cambio_venta),2) as total_soles,
#         '' AS observaciones,
#         (CASE WHEN MAX(cvb.nubefact) IS NOT NULL THEN MAX(cvb.nubefact) ELSE MAX(dgnr.respuesta->>'enlace') END) AS link_nubefact
#         FROM comprobante_venta_boletaventa cvb
#         LEFT JOIN datos_globales_seriescomprobante dgsc
#             ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
#         LEFT JOIN clientes_cliente cc
#             ON cc.id=cvb.cliente_id
#         LEFT JOIN comprobante_venta_boletaventadetalle cvbd
#             ON cvb.id=cvbd.boleta_venta_id
#         LEFT JOIN material_material mm
#             ON cvbd.content_type_id='%s' AND mm.id=cvbd.id_registro
#         LEFT JOIN datos_globales_tipocambiosunat dgtc
#             ON dgtc.fecha=cvb.fecha_emision
#         LEFT JOIN datos_globales_nubefactrespuesta dgnr
#             ON dgnr.content_type_id='%s' AND dgnr.id_registro=cvb.id AND dgnr.error=False AND dgnr.id=(select max(id) from datos_globales_nubefactrespuesta  where content_type_id='%s' AND id_registro=dgnr.id_registro AND dgnr.error=False)
#         WHERE cvb.sociedad_id='%s' AND '%s' <= cvb.fecha_emision AND cvb.fecha_emision <= '%s'
#         GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta)
#         ORDER BY fecha_orden, nro_comprobante  ;''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['material | material'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], global_sociedad, global_fecha_inicio, global_fecha_fin, DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['material | material'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], global_sociedad, global_fecha_inicio, global_fecha_fin)
#     query_info = FacturaVenta.objects.raw(sql)

#     info = []
#     for fila in query_info:
#         lista_datos = []
#         lista_datos.append(fila.fecha_emision_comprobante)
#         lista_datos.append(fila.tipo_comprobante)
#         lista_datos.append(fila.nro_comprobante)
#         lista_datos.append(fila.cliente_denominacion)
#         lista_datos.append(fila.ruc)
#         lista_datos.append(fila.productos)
#         lista_datos.append(fila.cantidad)
#         lista_datos.append(fila.precio_final)
#         lista_datos.append(fila.monto)
#         lista_datos.append(fila.igv)
#         lista_datos.append(fila.dscto_global)
#         lista_datos.append(fila.total_dolares)
#         lista_datos.append(fila.tipo_cambio_fact)
#         lista_datos.append(fila.total_soles)
#         lista_datos.append(fila.observaciones)
#         lista_datos.append(fila.link_nubefact)
#         info.append(lista_datos)

#     for fila in info:
#         if fila[2] not in list_anulados:
#             try:
#                 fila[8] = float(fila[8])
#                 fila[9] = float(fila[9])
#                 fila[10] =float(fila[10])
#                 fila[11] =float(fila[11])
#                 fila[12] = round(float(fila[12]),2)
#                 fila[13] = float(fila[13])
#             except:
#                 ''
#         else:
#             for i in range(16):
#                 if i == 3:
#                     fila[i] = 'ANULADO'
#                 elif i > 3:
#                     fila[i] = ''
#     return info

# def reporte_facturas_contador(global_sociedad, global_fecha_inicio, global_fecha_fin):

#     wb = Workbook()
#     #Para la primera hoja
#     hoja = wb.active
#     hoja.title = 'sheet'

#     # Encabezado
#     hoja.append(('FECHA', 'TIPO DE COMP.', 'N° COMPROB.', 'RAZON SOCIAL', 'RUC', 'PRODUCTOS', 'CANT.', 'PRECIO UNIT. (US$) CON IGV', 'MONTO (US$)', 'IGV (US$)', 'DESCUENTO GLOBAL', 'TOTAL (US$)', 'TIPO DE CAMBIO', 'MONTO SOLES (S/)', 'OBSERVACIONES', 'LINK')) # Crea la fila del encabezado con los títulos

#     # self.relleno_mc = PatternFill(start_color='FFCA0B', end_color='FFCA0B', fill_type='solid')
#     # wb['A1'].fill = redFill

#     # for cell in hoja['A1:N1']:
#     #     for _ in cell:
#     #         _.fill = redFill
    
#     color_relleno = rellenoSociedad(global_sociedad)

#     col_range = hoja.max_column  # get max columns in the worksheet
#     # cabecera de la tabla
#     for col in range(1, col_range + 1):
#         cell_header = hoja.cell(1, col)
#         cell_header.fill = color_relleno
#         cell_header.font = NEGRITA

#     info = consultaFacturasContador(global_sociedad, global_fecha_inicio, global_fecha_fin)
#     for producto in info:
#         hoja.append(producto) # Crea la fila del encabezado con los títulos

#     # A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8, J=9, K=10, L=11, M=12, N=13
#     for row in hoja.rows:
#         for col in range(hoja.max_column):
#             row[col].border = BORDE_DELGADO
#             if 8 <= col <=11:
#                 row[col].alignment = ALINEACION_DERECHA
#                 row[col].number_format = FORMATO_DOLAR
#             elif col == 13:
#                 row[col].alignment = ALINEACION_DERECHA
#                 row[col].number_format = FORMATO_SOLES
#             elif col == 15:
#                 if row[col].value != 'LINK':
#                     row[col].hyperlink =  row[col].value
#                     row[col].font =  COLOR_AZUL
#                 # print(row[col].value)
#                 # row[col].number_format = self.formato_soles
#         # # sheet.cell(fila,3).number_format = '$ #,##0.00'
#         # cell_N.number_format = self.formato_dolar

#     info2 = consultaNotasContador(global_sociedad, global_fecha_inicio, global_fecha_fin)
#     if info2 != []:
#         # cabecera de la tabla
#         hoja.append(('',)) # Crea la fila del encabezado con los títulos
#         hoja.append(('FECHA', 'TIPO DE COMP.', 'N° COMPROB.', 'RAZON SOCIAL', 'RUC', 'COMPROBANTE QUE SE MODIFICA', '', 'CANT.', 'DESCRIPCION', 'PRECIO UNIT. (US$) SIN IGV', 'DESCUENTO GLOBAL', 'VALOR DE VENTA (US$)', 'IGV (US$)', 'TOTAL (US$)', 'MOTIVO DE LA NOTA', 'LINK')) # Crea la fila del encabezado con los títulos
#         nueva_fila = hoja.max_row

#         for col in range(1, col_range + 1):
#             cell_header = hoja.cell(nueva_fila, col)
#             cell_header.fill = color_relleno
#             cell_header.font = NEGRITA

#         for fila in info2:
#             hoja.append(fila) # Crea la fila del encabezado con los títulos

#         for i in range(hoja.max_row):
#             if i >= nueva_fila-1:
#                 row = list(hoja.rows)[i]
#                 for col in range(hoja.max_column):
#                     row[col].border = BORDE_DELGADO
#                     if 10 <= col <=13:
#                         row[col].alignment = ALINEACION_DERECHA
#                         row[col].number_format = FORMATO_DOLAR
#                     elif col == 15:
#                         if row[col].value != 'LINK':
#                             row[col].hyperlink =  row[col].value
#                             row[col].font =  COLOR_AZUL
#     ajustarColumnasSheet(hoja)
#     return wb


# @background(schedule=60)  # Programa la tarea para ejecutarse cada 60 segundos (ajusta según tus necesidades)
# def generate_report(global_sociedad, global_fecha_inicio, global_fecha_fin):
#     # Coloca aquí la lógica de generación de informes
#     # Por ejemplo: wb = reporte_facturas_contador(global_sociedad, global_fecha_inicio, global_fecha_fin)
#     # Puedes guardar el informe en un lugar específico o realizar otras acciones

#     # Si deseas registrar el progreso o los resultados de la tarea, puedes hacerlo aquí

#     # Por ejemplo: logging.info("Informe generado correctamente")
    
#     query_sociedad = Sociedad.objects.filter(id=int(global_sociedad)).first()

#     if query_sociedad:
#         abreviatura = query_sociedad.abreviatura
#         wb = reporte_facturas_contador(global_sociedad, global_fecha_inicio, global_fecha_fin)

#         nombre_archivo = "Reporte Contador - " + abreviatura + " - " + datetime.now().strftime("%Y-%m-%d") + ".xlsx"
#         respuesta = HttpResponse(content_type='application/ms-excel')
#         content = "attachment; filename ={0}".format(nombre_archivo)
#         respuesta['content-disposition'] = content
#         wb.save(respuesta)
#         return respuesta