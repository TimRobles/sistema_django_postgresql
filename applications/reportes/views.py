from django.shortcuts import render
import time
from datetime import datetime, timedelta
from applications.importaciones import*
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Alignment
from openpyxl.styles import*
from openpyxl.styles.borders import Border, Side

from applications.datos_globales.models import CuentaBancariaSociedad
from applications.sociedad.models import Sociedad
from applications.cobranza.models import Pago
from applications.nota.models import NotaCredito
from applications.comprobante_venta.models import FacturaVenta
from django.contrib.contenttypes.models import ContentType

from applications.reportes.forms import ReportesFiltrosForm

from applications.reportes.funciones import*


class ReportesView(FormView):
    template_name = "reportes/inicio.html"
    form_class = ReportesFiltrosForm
    success_url = '.'

    def get_form_kwargs(self):
        kwargs = super(ReportesView, self).get_form_kwargs()
        # print('************************')
        # print(kwargs)
        # print('************************')
        
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        kwargs['filtro_fecha_inicio'] = self.request.GET.get('fecha_inicio')
        kwargs['filtro_fecha_fin'] = self.request.GET.get('fecha_fin')
        global global_sociedad, global_fecha_inicio, global_fecha_fin 
        global_sociedad = self.request.GET.get('sociedad')
        global_fecha_inicio = self.request.GET.get('fecha_inicio')
        global_fecha_fin = self.request.GET.get('fecha_fin')
        # print(kwargs['filtro_sociedad'])

        # print('************************')
        # print(self.request.GET.get('sociedad'))
        # print('************************')

        return kwargs

class ReporteContador(TemplateView):
    def get(self,request, *args,**kwargs):


        print('************************')
        global global_sociedad, global_fecha_inicio, global_fecha_fin
        print(global_sociedad, global_fecha_inicio, global_fecha_fin)
        print('************************')

        # print('##########################################')
        # print(DICT_CONTENT_TYPE)
        # print('##########################################')
        # wb = Workbook()
        # hoja = wb.active

        def prueba():
            # if global_sociedad == '2':
            #     color_relleno = RELLENO_MP
            # if global_sociedad == '1':
            #     color_relleno = RELLENO_MC

            # tabla_cuentas = CuentaBancariaSociedad.objects.raw('''SELECT id, banco_id, sociedad_id, numero_cuenta, numero_cuenta_interbancaria, moneda_id 
            # FROM datos_globales_cuentabancariasociedad 
            # WHERE estado='1' AND sociedad_id='%s' ;''' %('2')) 

            # info_cuentas = []
            # for fila in tabla_cuentas:
            #     lista_datos = []
            #     lista_datos.append(fila.banco)
            #     lista_datos.append(fila.sociedad)
            #     lista_datos.append(fila.numero_cuenta)
            #     lista_datos.append(fila.numero_cuenta_interbancaria)
            #     lista_datos.append(fila.moneda)
            #     info_cuentas.append(lista_datos)

            # print('***********************')
            # print(info_cuentas)
            # print('***********************')

            # list_temp_hojas = []
            # dict_totales_cuentas = {}
            # count_cuenta = 0
            # list_nro_cuentas = []
            # dict_nro_cuentas = {}
            # for fila in info_cuentas:
            #     nro_cuenta = fila[2]
            #     dict_nro_cuentas[nro_cuenta] = str(fila[0]) + ' ' +str(fila[4])
            #     list_nro_cuentas.append(nro_cuenta)

            #     tabla_depositos = Pago.objects.all()

            #     print('***********************')
            #     print(tabla_depositos)
            #     print('***********************')

                # sql_1 = ''' SELECT ci.fecha, ci.numero_operacion,
                #     SUM(ROUND(IF(dgm.abreviatura='USD', ci.monto, ci.monto/ci.tipo_cambio),2)) AS monto_dolares,
                #     SUM(ROUND(IF(dgm.abreviatura='USD', ci.monto*ci.tipo_cambio, ci.monto),2)) AS monto_soles,
                #     STRING_AGG(cd.cliente_id, '\n') AS empresas,
                #     STRING_AGG('FACTURA: ',dtsc.serie,'-',cvf.numero_factura, '\n') AS documentos,
                #     STRING_AGG(cvf.fecha_emision, '\n') AS fecha_documentos,
                #     STRING_AGG(ROUND(IF(dgm.abreviatura='USD', cp.monto, cp.monto/cp.tipo_cambio),2), '\n') AS pago_dolares,
                #     STRING_AGG(ROUND(IF(dgm.abreviatura='USD', cp.monto*cp.tipo_cambio, cp.monto),2), '\n') AS pago_soles
                #     FROM cobranza_pago cp
                #     LEFT JOIN cobranza_ingreso ci ON ci.id=cp.id_registro AND cp.content_type_id = 166
                #     LEFT JOIN datos_globales_cuentabancariasociedad dgcbs ON dgcbs.id=ci.cuenta_bancaria_id AND dgcbs.estado='1'
                #     LEFT JOIN datos_globales_moneda dgm ON dgm.id=dgcbs.moneda_id 
                #     LEFT JOIN cobranza_deuda cd ON cd.id = cp.deuda_id
                #     LEFT JOIN comprobante_venta_facturaventa cvf ON cvf.id = cd.id_registro AND cd.content_type_id = 168
                #     LEFT JOIN datos_globales_seriescomprobante dtsc ON dtsc.id = cvf.serie_comprobante_id
                #     LEFT JOIN datos_globales_banco dgb ON dgb.id = dgcbs.banco_id'''

                # sql_2 = ''' WHERE dgcbs.numero_cuenta='%s' AND CAST('%s' AS date) <= ci.fecha AND ci.fecha <= CAST('%s' AS date)
                #     GROUP BY ci.numero_operacion, dgcbs.banco_id, ci.cuenta_bancaria_id, ci.fecha
                #     ORDER BY ci.fecha ASC ;''' %(nro_cuenta, '2022-12-01', '2022-12-31')

                # sql_suma = sql_1 + sql_2
                # print('**************************')
                # print(sql_suma)
                # print('**************************')
                # info_depositos = Pago.objects.raw(sql_suma)
                # print('**************************')
                # print(info_depositos)
                # print('**************************')

                # for fila in info_depositos:
                #     print('**************************')
                #     print(fila)
                #     print('**************************')
            print()

        def consultaNotasContador():

            sql_1 = ''' SELECT
                MAX(nnc.id) AS id,
                to_char(MAX(nnc.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_nota,
                (CASE WHEN nnc.tipo_comprobante='3' THEN 'NOTA DE CRÉDITO' ELSE '-' END) as comprobante,
                CONCAT(MAX(dgsc.serie), '-', lpad(CAST(nnc.numero_nota AS TEXT), 6, '0')) as nro_comprobante,
                MAX(cc.razon_social) AS cliente_denominacion,
                MAX(cc.numero_documento) AS ruc,
                CONCAT(MAX(dgsc2.serie), '-', MAX(lpad(CAST(cvf.numero_factura AS TEXT), 6, '0'))) AS factura_modifica,
                '' AS obs,
                STRING_AGG(CAST(nncd.cantidad AS TEXT), ' | ') AS cantidad,
                STRING_AGG(mm.descripcion_corta, ' | ') AS productos,
                STRING_AGG(CAST(ROUND(nncd.precio_unitario_sin_igv, 2) AS TEXT), ' | ') AS precios,
                MAX(nnc.descuento_global) AS dscto_global,
                ROUND(SUM(nncd.sub_total), 2) AS valor_venta,
                SUM(nncd.igv)AS igv,
                ROUND(SUM(nncd.total), 2) AS total_venta,
                MAX(nnc.tipo_nota_credito) AS motivo_nota,
                MAX(nnc.nubefact) AS url_nota
                FROM nota_notacredito nnc
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=nnc.serie_comprobante_id AND dgsc.id='10'
                LEFT JOIN clientes_cliente cc
                    ON cc.id=nnc.cliente_id
                LEFT JOIN datos_globales_documentofisico dgdf
                    ON dgdf.id=nnc.content_type_documento_id AND dgdf.modelo_id='%s'
                LEFT JOIN comprobante_venta_facturaventa cvf
                    ON cvf.id=nnc.id_registro_documento
                LEFT JOIN datos_globales_seriescomprobante dgsc2
                    ON dgsc2.tipo_comprobante_id='%s' AND dgsc2.id=cvf.serie_comprobante_id
                LEFT JOIN nota_notacreditodetalle nncd
                    ON nnc.id=nncd.nota_credito_id
                LEFT JOIN material_material mm
                    ON nncd.content_type_id='%s' AND mm.id=nncd.id_registro ''' %(DICT_CONTENT_TYPE['nota | notacredito'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['material | material'])
            sql_2 = ''' WHERE nnc.sociedad_id='%s' AND '%s' <= nnc.fecha_emision AND nnc.fecha_emision <= '%s'
                GROUP BY nnc.sociedad_id, nnc.tipo_comprobante, nnc.serie_comprobante_id, nnc.numero_nota ;''' %(global_sociedad,global_fecha_inicio, global_fecha_fin)
            sql = sql_1 + sql_2
            query_info = NotaCredito.objects.raw(sql)
            
            info = []
            for fila in query_info:
                lista_datos = []
                lista_datos.append(fila.fecha_emision_nota)
                lista_datos.append(fila.comprobante)
                lista_datos.append(fila.nro_comprobante)
                lista_datos.append(fila.cliente_denominacion)
                lista_datos.append(fila.ruc)
                lista_datos.append(fila.factura_modifica)
                lista_datos.append(fila.obs)
                lista_datos.append(fila.cantidad)
                lista_datos.append(fila.productos)
                lista_datos.append(fila.precios)
                lista_datos.append(fila.dscto_global)
                lista_datos.append(fila.valor_venta)
                lista_datos.append(fila.igv)
                lista_datos.append(fila.total_venta)
                lista_datos.append(fila.motivo_nota)
                lista_datos.append(fila.url_nota)
                info.append(lista_datos)

            for fila in info:
                fila[10] =float(fila[10])
                fila[11] =float(fila[11])
                fila[12] = float(fila[12])
                fila[13] = float(fila[13])
                fila[14] = DICT_TIPO_NOTA_CREDITO[fila[14]]
            return info


        def consultaFacturasContador():
            # global_fecha_inicio = '2022-01-01'
            # global_fecha_fin = '2022-01-31'

            sql_anuladas = ''' (SELECT
                MAX(cvf.id) as id,
                CONCAT(MAX(dgsc.serie), '-', MAX(lpad(CAST(cvf.numero_factura AS TEXT), 6, '0'))) as nro_comprobante
                FROM comprobante_venta_facturaventa cvf
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
                WHERE cvf.estado='3' and cvf.sociedad_id='%s')
                UNION
                (SELECT
                MAX(cvb.id) as id,
                CONCAT(MAX(dgsc.serie), '-', MAX(lpad(CAST(cvb.numero_boleta AS TEXT), 6, '0'))) as nro_comprobante
                FROM comprobante_venta_boletaventa cvb
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
                WHERE cvb.estado='3' and cvb.sociedad_id='%s') ; ''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], global_sociedad, DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], global_sociedad)
            query_info_anulados = FacturaVenta.objects.raw(sql_anuladas)

            list_temp = []
            info_anulados = []
            for fila in query_info_anulados:
                list_temp.append(fila.nro_comprobante)
                info_anulados.append(list_temp)  

            # print('****************************')
            # print(info_anulados)
            # print('****************************')

            list_anulados = []
            for fact in info_anulados:
                list_anulados.append(fact[0])

            sql_1 = ''' (SELECT
                MAX(cvf.id) AS id,
                to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                'FACTURA' AS tipo_comprobante,
                CONCAT(MAX(dgsc.serie), '-', MAX(lpad(CAST(cvf.numero_factura AS TEXT), 6, '0'))) AS nro_comprobante,
                MAX(cc.razon_social) AS cliente_denominacion,
                MAX(cc.numero_documento) AS ruc,
                STRING_AGG(mm.descripcion_corta, ' | ') AS productos,
                STRING_AGG(CAST(cvfd.cantidad AS TEXT), ' | ') AS cantidad,
                STRING_AGG(CAST(ROUND(cvfd.precio_final_con_igv, 2) AS TEXT), ' | ') AS precio_final,
                ROUND((SUM(cvfd.total)-ROUND((MAX(cvf.descuento_global)*1.18),2))/1.18,2) AS monto,
                MAX(cvf.total_igv) AS igv,
                MAX(cvf.descuento_global) AS dscto_global,
                SUM(cvfd.total)-ROUND((MAX(cvf.descuento_global)*1.18),2) AS total_dolares,
                ROUND(MAX(dgtc.tipo_cambio_venta), 2) AS tipo_cambio_fact,
                ROUND((SUM(cvfd.total)-ROUND((MAX(cvf.descuento_global)*1.18),2))*MAX(dgtc.tipo_cambio_venta),2) AS total_soles,
                '' AS observaciones,
                MAX(cvf.nubefact) AS link_nubefact
                FROM comprobante_venta_facturaventa cvf
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
                LEFT JOIN clientes_cliente cc
                    ON cc.id=cvf.cliente_id
                LEFT JOIN comprobante_venta_facturaventadetalle cvfd
                    ON cvf.id=cvfd.factura_venta_id
                LEFT JOIN material_material mm
                    ON cvfd.content_type_id='%s' AND mm.id=cvfd.id_registro
                LEFT JOIN datos_globales_tipocambio dgtc
                    ON dgtc.id=cvf.tipo_cambio_id ''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['material | material'])
            sql_2 = ''' WHERE cvf.sociedad_id='%s' AND '%s' <= cvf.fecha_emision AND cvf.fecha_emision <= '%s'
                GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura) ''' %(global_sociedad, global_fecha_inicio, global_fecha_fin)
            sql_3 = ''' UNION
                (SELECT
                MAX(cvb.id) as id,
                to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                'BOLETA' AS tipo_comprobante,
                CONCAT(MAX(dgsc.serie), '-', MAX(lpad(CAST(cvb.numero_boleta AS TEXT), 6, '0'))) as nro_comprobante,
                MAX(cc.razon_social) AS cliente_denominacion,
                MAX(cc.numero_documento) AS ruc,
                STRING_AGG(mm.descripcion_corta, ' | ') AS productos,
                STRING_AGG(CAST(cvbd.cantidad AS TEXT), ' | ') AS cantidad,
                STRING_AGG(CAST(ROUND(cvbd.precio_final_con_igv, 2) AS TEXT), ' | ') AS precio_final,
                ROUND((SUM(cvbd.total)-ROUND((MAX(cvb.descuento_global)*1.18),2))/1.18,2) AS monto,
                MAX(cvb.total_igv) AS igv,
                MAX(cvb.descuento_global) AS dscto_global,
                SUM(cvbd.total)-ROUND((MAX(cvb.descuento_global)*1.18),2) AS total_dolares,
                ROUND(MAX(dgtc.tipo_cambio_venta), 2) AS tipo_cambio_fact,
                ROUND((SUM(cvbd.total)-ROUND((MAX(cvb.descuento_global)*1.18),2))*MAX(dgtc.tipo_cambio_venta),2) as total_soles,
                '' AS observaciones,
                MAX(cvb.nubefact)
                FROM comprobante_venta_boletaventa cvb
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
                LEFT JOIN clientes_cliente cc
                    ON cc.id=cvb.cliente_id
                LEFT JOIN comprobante_venta_boletaventadetalle cvbd
                    ON cvb.id=cvbd.boleta_venta_id
                LEFT JOIN material_material mm
                    ON cvbd.content_type_id='%s' AND mm.id=cvbd.id_registro
                LEFT JOIN datos_globales_tipocambio dgtc
                    ON dgtc.id=cvb.tipo_cambio_id ''' %(DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['material | material'])
            sql_4 = ''' WHERE cvb.sociedad_id='%s' AND '%s' <= cvb.fecha_emision AND cvb.fecha_emision <= '%s'
                GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta)
                ORDER BY fecha_emision_comprobante ;''' %(global_sociedad, global_fecha_inicio, global_fecha_fin)
                
                # WHERE cf.Nro_Facturacion='001454'
            sql = sql_1 + sql_2 + sql_3 + sql_4
            query_info = FacturaVenta.objects.raw(sql)

            info = []
            for fila in query_info:
                lista_datos = []
                lista_datos.append(fila.fecha_emision_comprobante)
                lista_datos.append(fila.tipo_comprobante)
                lista_datos.append(fila.nro_comprobante)
                lista_datos.append(fila.cliente_denominacion)
                lista_datos.append(fila.ruc)
                lista_datos.append(fila.productos)
                lista_datos.append(fila.cantidad)
                lista_datos.append(fila.precio_final)
                lista_datos.append(fila.monto)
                lista_datos.append(fila.igv)
                lista_datos.append(fila.dscto_global)
                lista_datos.append(fila.total_dolares)
                lista_datos.append(fila.tipo_cambio_fact)
                lista_datos.append(fila.total_soles)
                lista_datos.append(fila.observaciones)
                lista_datos.append(fila.link_nubefact)
                info.append(lista_datos)

            for fila in info:
                if fila[2] not in list_anulados:
                    try:
                        fila[8] = float(fila[8])
                        fila[9] = float(fila[9])
                        fila[10] =float(fila[10])
                        fila[11] =float(fila[11])
                        fila[12] = round(float(fila[12]),2)
                        fila[13] = float(fila[13])
                    except:
                        ''
                else:
                    for i in range(16):
                        if i == 3:
                            fila[i] = 'ANULADO'
                        elif i > 3:
                            fila[i] = ''
            return info


        def reporte_facturas_contador():

            wb = Workbook()
            #Para la primera hoja
            hoja = wb.active
            hoja.title = 'sheet'

            # Encabezado
            hoja.append(('FECHA', 'TIPO DE COMP.', 'N° COMPROB.', 'RAZON SOCIAL', 'RUC', 'PRODUCTOS', 'CANT.', 'PRECIO UNIT. (US$) CON IGV', 'MONTO (US$)', 'IGV (US$)', 'DESCUENTO GLOBAL', 'TOTAL (US$)', 'TIPO DE CAMBIO', 'MONTO SOLES (S/)', 'OBSERVACIONES', 'LINK')) # Crea la fila del encabezado con los títulos

            # self.relleno_mc = PatternFill(start_color='FFCA0B', end_color='FFCA0B', fill_type='solid')
            # wb['A1'].fill = redFill

            # for cell in hoja['A1:N1']:
            #     for _ in cell:
            #         _.fill = redFill

            if global_sociedad == '2':
                color_relleno = RELLENO_MP
            if global_sociedad == '1':
                color_relleno = RELLENO_MC

            col_range = hoja.max_column  # get max columns in the worksheet
            # cabecera de la tabla
            for col in range(1, col_range + 1):
                cell_header = hoja.cell(1, col)
                cell_header.fill = color_relleno
                cell_header.font = NEGRITA

            info = consultaFacturasContador()
            for producto in info:
                hoja.append(producto) # Crea la fila del encabezado con los títulos

            # A=0, B=1, C=2, D=3, E=4, F=5, G=6, H=7, I=8, J=9, K=10, L=11, M=12, N=13
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
                        # print(row[col].value)
                        # row[col].number_format = self.formato_soles
                # # sheet.cell(fila,3).number_format = '$ #,##0.00'
                # cell_N.number_format = self.formato_dolar

            info2 = consultaNotasContador()
            if info2 != []:
                # cabecera de la tabla
                hoja.append(('',)) # Crea la fila del encabezado con los títulos
                hoja.append(('FECHA', 'TIPO DE COMP.', 'N° COMPROB.', 'RAZON SOCIAL', 'RUC', 'FACTURA QUE SE MODIFICA', '', 'CANT.', 'DESCRIPCION', 'PRECIO UNIT. (US$) SIN IGV', 'DESCUENTO GLOBAL', 'VALOR DE VENTA (US$)', 'IGV (US$)', 'TOTAL (US$)', 'MOTIVO DE LA NOTA', 'LINK')) # Crea la fila del encabezado con los títulos
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

        query_sociedad = Sociedad.objects.filter(id = int(global_sociedad))[0]
        abreviatura = query_sociedad.abreviatura
        wb=reporte_facturas_contador()
        nombre_archivo = "Reporte_Contador - " + abreviatura + " - " + FECHA_HOY + ".xlsx"
        respuesta = HttpResponse(content_type='application/ms-excel')
        content = "attachment; filename ={0}".format(nombre_archivo)
        respuesta['content-disposition']= content
        wb.save(respuesta)
        return respuesta

class ReporteVentasFacturadas(TemplateView):
    def get(self,request, *args,**kwargs):
        global global_sociedad, global_fecha_inicio, global_fecha_fin

        def consulta_ventas_notas():
            sql = ''' SELECT
                MAX(nnc.id) AS id,
                to_char(MAX(nnc.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_nota,
                (CASE WHEN nnc.tipo_comprobante='3' THEN 'NOTA DE CRÉDITO' ELSE '-' END) as comprobante,
                CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(nnc.numero_nota) AS TEXT), 6, '0')) as nro_comprobante,
                MAX(cc.razon_social) AS cliente_denominacion,
                (SUM(nncd.total)*(-1)) AS facturado,
                (SUM(nncd.total)*(-1)) AS amortizado,
                '0.00' AS pendiente,
                'PENDIENTE' AS estado,
                to_char(MAX(nnc.fecha_vencimiento), 'DD/MM/YYYY') AS fecha_vencimiento_nota,
                '0.00' AS credito,
                '' AS dias,
                '' AS guia,
                '' AS obs,
                '' AS letras,
                '' AS pagos
                FROM nota_notacredito nnc
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=nnc.serie_comprobante_id AND dgsc.id='10'
                LEFT JOIN nota_notacreditodetalle nncd
                    ON nnc.id=nncd.nota_credito_id
                LEFT JOIN clientes_cliente cc
                    ON cc.id=nnc.cliente_id
                WHERE nnc.sociedad_id='%s' AND '%s' <= nnc.fecha_emision AND nnc.fecha_emision <= '%s'
                GROUP BY nnc.sociedad_id, nnc.tipo_comprobante, nnc.serie_comprobante_id, nnc.numero_nota ; ''' %(DICT_CONTENT_TYPE['nota | notacredito'], global_sociedad, global_fecha_inicio, global_fecha_fin)

            query_info = NotaCredito.objects.raw(sql)
            
            info = []
            for fila in query_info:
                lista_datos = []
                lista_datos.append(fila.fecha_emision_nota)
                lista_datos.append(fila.comprobante)
                lista_datos.append(fila.nro_comprobante)
                lista_datos.append(fila.cliente_denominacion)
                lista_datos.append(fila.facturado)
                lista_datos.append(fila.amortizado)
                lista_datos.append(fila.pendiente)
                lista_datos.append(fila.estado)
                lista_datos.append(fila.fecha_vencimiento_nota)
                lista_datos.append(fila.credito)
                lista_datos.append(fila.dias)
                lista_datos.append(fila.guia)
                lista_datos.append(fila.obs)
                lista_datos.append(fila.letras)
                lista_datos.append(fila.pagos)
                info.append(lista_datos)

            for fila in info:
                try:
                    fila[4] = float(fila[4])
                    fila[5] = float(fila[5])
                    fila[6] = float(fila[6])
                    fila[9] = float(fila[9])
                except:
                    ''
            return info

        def reporte_ventas():
            info_notas = consulta_ventas_notas()
            # FECHA_INICIO = '2021-12-20'
            # FECHA_FIN = '2022-01-31'
            # sql = ''' SELECT cf.Fecha_Emision, IF(cf.Tipo_Comprobante='1','Factura','Boleta') AS comprobante, CONCAT(cf.Serie, '-', cf.Nro_Facturacion) AS nro_comprobante,
            #     mc.Razon_Social, SUM(df.Sub_Total)-ROUND((cf.Descuento_Global*1.18),2) as facturado, SUM(cob.Monto_Deposito) as total, SUM(cob.Monto_Deposito)-SUM(cob.Monto_Saldo) AS amoritzado, SUM(cob.Monto_Saldo) AS pendiente, IF(SUM(cob.Monto_Saldo)=0.00,'CANCELADO','PENDIENTE') as estado, cf.Fecha_Vencimiento, CONCAT(cg.Serie,'-',cg.Nro_Guia) AS guia, cg.Fecha_Emision, GROUP_CONCAT(CONCAT(dob.Fecha_Operacion,'  $ ',dob.Monto_Deposito) SEPARATOR ' | ')
            # 	FROM `TAB_VENTA_009_Cabecera_Facturacion` cf
            #     LEFT JOIN TAB_VENTA_010_Detalle_Facturacion df
            #         ON cf.Cod_Soc=df.Cod_Soc AND cf.Año=df.Año AND cf.Tipo_Comprobante=df.Tipo_Comprobante AND cf.Serie=df.Serie AND cf.Nro_Facturacion=df.Nro_Facturacion
            #     LEFT JOIN `TAB_COM_001_Maestro Clientes` mc ON cf.Cod_Cliente=mc.Cod_Cliente
            #     LEFT JOIN TAB_VENTA_005_Cabecera_Operaciones_Bancarias_Por_Cotizacion cob ON cob.Cod_Soc=cf.Cod_Soc AND LEFT(cf.Nro_Cotización,4)=cob.Año_Cot_Client AND MID(cf.Nro_Cotización,6,10)=cob.Nro_Cot_Client AND cf.Cod_Cliente=cob.Cod_Cliente
            #     LEFT JOIN TAB_VENTA_006_Detalle_Operaciones_Bancarias_Por_Cotizacion dob ON cob.Cod_Soc=dob.Cod_Emp AND dob.Año_Cot_Client=cob.Año_Cot_Client AND dob.Nro_Cot_Client=cob.Nro_Cot_Client AND dob.Cod_Cliente=cob.Cod_Cliente
            #     LEFT JOIN TAB_VENTA_013_Cabecera_Guia_Remision cg ON CONCAT(cf.Serie,'-',cf.Nro_Facturacion)=cg.Doc_Referencia
            #     WHERE cf.Fecha_Emision != '0000-00-00' AND cf.Cod_Soc='2000'
            #     GROUP BY cf.Cod_Soc, cf.Año, cf.Tipo_Comprobante, cf.Serie, cf.Nro_Facturacion, cob.Cod_Soc, cob.Año_Cot_Client, cob.Nro_Cot_Client, dob.Cod_Emp ;'''

            sql_anuladas = ''' (SELECT
                MAX(cvf.id) AS id,
                CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT), 6, '0')) as nro_comprobante
                FROM comprobante_venta_facturaventa cvf
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
                WHERE cvf.estado='3' and cvf.sociedad_id='%s')
                UNION
                (SELECT
                MAX(cvb.id) AS id,
                CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT), 6, '0')) as nro_comprobante
                FROM comprobante_venta_boletaventa cvb
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
                WHERE cvb.estado='3' and cvb.sociedad_id='%s') ; '''%(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], global_sociedad, DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], global_sociedad)
            query_info_anulados = FacturaVenta.objects.raw(sql_anuladas)

            list_temp = []
            info_anulados = []
            for fila in query_info_anulados:
                list_temp.append(fila.nro_comprobante)
                info_anulados.append(list_temp)  

            list_anulados = []
            for fact in info_anulados:
                list_anulados.append(fact[0])

            sql_pagos = ''' (SELECT
                MAX(cvf.id) AS id, 
                to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                'FACTURA' AS tipo_comprobante,
                CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT), 6, '0')) as nro_comprobante,
                MAX(cc.razon_social) AS cliente_denominacion,
                STRING_AGG(CONCAT(
                            to_char(ci.fecha, 'DD/MM/YYYY'),
                            CONCAT(' ', dgm.simbolo, CAST(ROUND(cp.monto,2) AS TEXT)),
                        (CASE WHEN dgm.abreviatura='PEN'
                        THEN (
                            CONCAT(' ($ ', CAST(ROUND(cp.monto/cp.tipo_cambio,2) AS TEXT), ')')
                        ) ELSE (
                            ''
                        ) END)
                        ), '\n') AS pagos
                FROM comprobante_venta_facturaventa cvf
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
                LEFT JOIN clientes_cliente cc
                    ON cc.id=cvf.cliente_id
                LEFT JOIN cobranza_deuda cd
                    ON cd.content_type_id='%s' AND cd.id_registro=cvf.id
                LEFT JOIN cobranza_pago cp
                    ON cp.deuda_id=cd.id AND cp.content_type_id='%s'
                LEFT JOIN cobranza_ingreso ci
                    ON ci.id=cp.id_registro
                LEFT JOIN datos_globales_cuentabancariasociedad dgcb
                    ON dgcb.id=ci.cuenta_bancaria_id
                LEFT JOIN datos_globales_moneda dgm
                    ON dgm.id=dgcb.moneda_id
                WHERE cvf.sociedad_id='%s'
                GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura
                ORDER BY cliente_denominacion ASC, pagos DESC )
                UNION
                (SELECT 
                MAX(cvb.id) AS id,
                to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                'BOLETA' AS tipo_comprobante,
                CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT), 6, '0')) as nro_comprobante,
                MAX(cc.razon_social) AS cliente_denominacion,
                STRING_AGG(CONCAT(
                            to_char(ci.fecha, 'DD/MM/YYYY'),
                            CONCAT(' ', dgm.simbolo, CAST(ROUND(cp.monto,2) AS TEXT)),
                        (CASE WHEN dgm.abreviatura='PEN'
                        THEN (
                            CONCAT(' ($ ', CAST(ROUND(cp.monto/cp.tipo_cambio,2) AS TEXT), ')')
                        ) ELSE (
                            ''
                        ) END)
                        ), '\n') AS pagos
                FROM comprobante_venta_boletaventa cvb
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
                LEFT JOIN clientes_cliente cc
                    ON cc.id=cvb.cliente_id
                LEFT JOIN cobranza_deuda cd
                    ON cd.content_type_id='%s' AND cd.id_registro=cvb.id
                LEFT JOIN cobranza_pago cp
                    ON cp.deuda_id=cd.id AND cp.content_type_id='%s'
                LEFT JOIN cobranza_ingreso ci
                    ON ci.id=cp.id_registro
                LEFT JOIN datos_globales_cuentabancariasociedad dgcb
                    ON dgcb.id=ci.cuenta_bancaria_id
                LEFT JOIN datos_globales_moneda dgm
                    ON dgm.id=dgcb.moneda_id
                WHERE cvb.sociedad_id='%s'
                GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta
                ORDER BY cliente_denominacion ASC, pagos DESC)
                ORDER BY cliente_denominacion ASC, pagos DESC; '''%(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['cobranza | ingreso'], global_sociedad,  DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['cobranza | ingreso'], global_sociedad)
            query_info_pagos = FacturaVenta.objects.raw(sql_pagos)

            info = []
            for fila in query_info_pagos:
                lista_datos = []
                lista_datos.append(fila.fecha_emision_comprobante)
                lista_datos.append(fila.tipo_comprobante)
                lista_datos.append(fila.nro_comprobante)
                lista_datos.append(fila.cliente_denominacion)
                lista_datos.append(fila.pagos)
                info.append(lista_datos)

            dict_pagos = {}
            for fila in info:
                dict_pagos[fila[0]+'|'+fila[1]+'|'+fila[2]] = fila[4]


            sql_letras = ''' (SELECT 
                MAX(cvf.id) AS id,
                to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                'FACTURA' AS tipo_comprobante,
                CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) AS nro_comprobante,
                (CASE WHEN MAX(cvf.tipo_venta)='2'
                THEN (
                    STRING_AGG(CONCAT(
                        to_char(cobc.fecha, 'DD/MM/YYYY'),
                        ' $ ',
                        CAST(ROUND(cobc.monto,2) AS TEXT)
                        ), '\n')
                ) ELSE (
                    ''
                ) END) AS letras
                FROM comprobante_venta_facturaventa cvf
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
                LEFT JOIN clientes_cliente cc
                    ON cc.id=cvf.cliente_id
                LEFT JOIN cobranza_deuda cd
                    ON cd.content_type_id='%s' AND cd.id_registro=cvf.id
                LEFT JOIN cobranza_cuota cobc
                    ON cobc.deuda_id=cd.id
                WHERE cvf.tipo_venta='2' AND cvf.sociedad_id='%s' AND '%s' <= cvf.fecha_emision AND cvf.fecha_emision <= '%s'
                GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura
                ORDER BY fecha_emision_comprobante ASC, nro_comprobante ASC)
                UNION
                (SELECT 
                MAX(cvb.id) AS id,
                to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                'BOLETA' AS tipo_comprobante,
                CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT),6,'0')) AS nro_comprobante,
                (CASE WHEN MAX(cvb.tipo_venta)='2'
                THEN (
                    STRING_AGG(CONCAT(
                        to_char(cobc.fecha, 'DD/MM/YYYY'),
                        ' $ ',
                        CAST(ROUND(cobc.monto,2) AS TEXT)
                        ), '\n')
                ) ELSE (
                    ''
                ) END) AS letras
                FROM comprobante_venta_boletaventa cvb
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
                LEFT JOIN clientes_cliente cc
                    ON cc.id=cvb.cliente_id
                LEFT JOIN cobranza_deuda cd
                    ON cd.content_type_id='%s' AND cd.id_registro=cvb.id
                LEFT JOIN cobranza_cuota cobc
                    ON cobc.deuda_id=cd.id
                WHERE cvb.tipo_venta='2' AND cvb.sociedad_id='%s' AND '%s' <= cvb.fecha_emision AND cvb.fecha_emision <= '%s'
                GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta
                ORDER BY fecha_emision_comprobante ASC, nro_comprobante ASC) ; ''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], global_sociedad, global_fecha_inicio, global_fecha_fin, DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], global_sociedad, global_fecha_inicio, global_fecha_fin)

            query_info_letras = FacturaVenta.objects.raw(sql_letras)

            info = []
            for fila in query_info_letras:
                lista_datos = []
                lista_datos.append(fila.fecha_emision_comprobante)
                lista_datos.append(fila.tipo_comprobante)
                lista_datos.append(fila.nro_comprobante)
                lista_datos.append(fila.letras)
                info.append(lista_datos)

            dict_letras = {}
            for fila in info:
                dict_letras[fila[0]+'|'+fila[1]+'|'+fila[2]] = fila[3]

            sql_facturas = ''' (SELECT 
                MAX(cvf.id) AS id,
                to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                'FACTURA' AS tipo_comprobante,
                CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) AS nro_comprobante,
                MAX(cc.razon_social) AS cliente_denominacion,
                MAX(cvf.total) AS monto_facturado,
                SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) + SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_amortizado,
                MAX(cvf.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_pendiente,
                (CASE WHEN CAST(ROUND(MAX(cvf.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END), 2) AS TEXT)='0.00'
                    THEN (
                        'CANCELADO'
                    ) ELSE (
                        'PENDIENTE'
                    ) END) AS estado_cobranza,
                to_char(MAX(cvf.fecha_vencimiento), 'DD/MM/YYYY') AS fecha_vencimiento_comprobante,
                EXTRACT(DAY FROM MAX(cvf.fecha_vencimiento)) - EXTRACT(DAY FROM MAX(cvf.fecha_emision)) AS dias_credito,
                MAX(cvf.fecha_vencimiento) AS dias_vencimiento,
                STRING_AGG(
                    DISTINCT(CONCAT(dgsc2.serie, '-', lpad(CAST(cdg.numero_guia AS TEXT),6,'0'), ' ', to_char(cdg.fecha_emision, 'DD/MM/YYYY'))), '\n') AS guias,
                '' AS letras,
                '' AS pagos
                FROM comprobante_venta_facturaventa cvf
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
                LEFT JOIN clientes_cliente cc
                    ON cc.id=cvf.cliente_id
                LEFT JOIN cobranza_deuda cd
                    ON cd.content_type_id='%s' AND cd.id_registro=cvf.id
                LEFT JOIN cobranza_pago cp
                    ON cp.deuda_id=cd.id AND cp.content_type_id='%s'
                LEFT JOIN cobranza_ingreso ci
                    ON ci.id=cp.id_registro
                LEFT JOIN datos_globales_cuentabancariasociedad dgcb
                    ON dgcb.id=ci.cuenta_bancaria_id
                LEFT JOIN datos_globales_moneda dgm
                    ON dgm.id=dgcb.moneda_id
                LEFT JOIN cobranza_redondeo cr
                    ON cr.deuda_id=cd.id
                LEFT JOIN logistica_notasalida lns
                    ON lns.confirmacion_venta_id=cvf.confirmacion_id
                LEFT JOIN logistica_despacho ld
                    ON ld.nota_salida_id=lns.id
                LEFT JOIN comprobante_despacho_guia cdg
                    ON cdg.despacho_id=ld.id
                LEFT JOIN datos_globales_seriescomprobante dgsc2
                    ON dgsc2.tipo_comprobante_id='%s' AND dgsc2.id=cdg.serie_comprobante_id
                WHERE cvf.sociedad_id='%s' AND '%s' <= cvf.fecha_emision AND cvf.fecha_emision <= '%s'
                GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura
                ORDER BY fecha_emision_comprobante ASC, nro_comprobante ASC)
                UNION
                (SELECT 
                MAX(cvb.id) AS id,
                to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                'BOLETA' AS tipo_comprobante,
                CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT),6,'0')) AS nro_comprobante,
                MAX(cc.razon_social) AS cliente_denominacion,
                MAX(cvb.total) AS monto_facturado,
                SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) + SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_amortizado,
                MAX(cvb.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_pendiente,
                (CASE WHEN CAST(ROUND(MAX(cvb.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END), 2) AS TEXT)='0.00'
                    THEN (
                        'CANCELADO'
                    ) ELSE (
                        'PENDIENTE'
                    ) END) AS estado_cobranza,
                to_char(MAX(cvb.fecha_vencimiento), 'DD/MM/YYYY') AS fecha_vencimiento_comprobante,
                EXTRACT(DAY FROM MAX(cvb.fecha_vencimiento)) - EXTRACT(DAY FROM MAX(cvb.fecha_emision)) AS dias_credito,
                MAX(cvb.fecha_vencimiento) AS dias_vencimiento,
                STRING_AGG(
                    DISTINCT(CONCAT(dgsc2.serie, '-', lpad(CAST(cdg.numero_guia AS TEXT),6,'0'), ' ', to_char(cdg.fecha_emision, 'DD/MM/YYYY'))), '\n') AS guias,
                '' AS letras,
                '' AS pagos
                FROM comprobante_venta_boletaventa cvb
                LEFT JOIN datos_globales_seriescomprobante dgsc
                    ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
                LEFT JOIN clientes_cliente cc
                    ON cc.id=cvb.cliente_id
                LEFT JOIN cobranza_deuda cd
                    ON cd.content_type_id='%s' AND cd.id_registro=cvb.id
                LEFT JOIN cobranza_pago cp
                    ON cp.deuda_id=cd.id AND cp.content_type_id='%s'
                LEFT JOIN cobranza_ingreso ci
                    ON ci.id=cp.id_registro
                LEFT JOIN datos_globales_cuentabancariasociedad dgcb
                    ON dgcb.id=ci.cuenta_bancaria_id
                LEFT JOIN datos_globales_moneda dgm
                    ON dgm.id=dgcb.moneda_id
                LEFT JOIN cobranza_redondeo cr
                    ON cr.deuda_id=cd.id
                LEFT JOIN logistica_notasalida lns
                    ON lns.confirmacion_venta_id=cvb.confirmacion_id
                LEFT JOIN logistica_despacho ld
                    ON ld.nota_salida_id=lns.id
                LEFT JOIN comprobante_despacho_guia cdg
                    ON cdg.despacho_id=ld.id
                LEFT JOIN datos_globales_seriescomprobante dgsc2
                    ON dgsc2.tipo_comprobante_id='%s' AND dgsc2.id=cdg.serie_comprobante_id
                WHERE cvb.sociedad_id='%s' AND '%s' <= cvb.fecha_emision AND cvb.fecha_emision <= '%s'
                GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta
                ORDER BY fecha_emision_comprobante ASC, nro_comprobante ASC) ; ''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['cobranza | ingreso'], DICT_CONTENT_TYPE['comprobante_despacho | guia'], global_sociedad, global_fecha_inicio, global_fecha_fin, DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['cobranza | ingreso'], DICT_CONTENT_TYPE['comprobante_despacho | guia'], global_sociedad, global_fecha_inicio, global_fecha_fin)
            query_info_facturas = FacturaVenta.objects.raw(sql_facturas)
            
            info_facturas = []
            for fila in query_info_facturas:
                lista_datos = []
                lista_datos.append(fila.fecha_emision_comprobante)
                lista_datos.append(fila.tipo_comprobante)
                lista_datos.append(fila.nro_comprobante)
                lista_datos.append(fila.cliente_denominacion)
                lista_datos.append(fila.monto_facturado)
                lista_datos.append(fila.monto_amortizado)
                lista_datos.append(fila.monto_pendiente)
                lista_datos.append(fila.estado_cobranza)
                lista_datos.append(fila.fecha_vencimiento_comprobante)
                lista_datos.append(fila.dias_credito)
                lista_datos.append(fila.dias_vencimiento)
                lista_datos.append(fila.guias)
                lista_datos.append(fila.letras)
                lista_datos.append(fila.pagos)
                info_facturas.append(lista_datos)

            # dict_comprobante = {
            #     'Factura': '1',
            #     'Boleta': '2',
            #     }
            for fila in info_facturas:
                if fila[2] not in list_anulados:
                    try:
                        fila[4] = float(fila[4])
                        fila[5] = float(fila[5])
                        fila[6] = float(fila[6])
                        fila[9] = float(fila[9])
                    except:
                        ''
                    if fila[10] != '':
                        fecha_hoy = time.strftime("%Y-%m-%d")
                        fecha1 = datetime.strptime(fecha_hoy, '%Y-%m-%d')
                        fecha2 = datetime.strptime(fila[10], '%Y-%m-%d')
                        dias = (fecha1 - fecha2) / timedelta(days=1)
                        if float(fila[9]) == float(0):
                            fila[10] = ''
                        elif fila[7] != 'CANCELADO':
                            fila[10] = float(dias)
                        else:
                            fila[10] = ''
                    if float(dias) > float(0) and fila[7]=='PENDIENTE':
                        fila[7] = 'VENCIDO'
                    fila[13] = dict_pagos[fila[0]+'|'+fila[1]+'|'+fila[2]]
                else:
                    for i in range(13):
                        if i == 3:
                            fila[i] = 'ANULADO'
                        elif i > 3:
                            fila[i] = ''

            info = info_facturas + info_notas
            info_ordenado = sorted(info, key=lambda x:formatearFecha3(x[0]))

            wb = Workbook()

            count = 0
            list_general = []
            list_temp = []
            for fila in info_ordenado:
                if count != 0:
                    if fila[0][3:5] != info_ordenado[count-1][0][3:5]:
                        list_general.append(list_temp)
                        list_temp = []
                list_temp.append(fila)
                count += 1
            list_general.append(list_temp)
            # if list_general == [] and list_temp != []:
                # list_general.append(list_temp)
            # print('Listas encontradas:',len(list_general))

            count = 0
            total_facturado = 0
            list_montos_totales = []
            for info in list_general:
                name_sheet = DICT_MESES[str(info[0][0][3:5])] + ' - ' + str(info[0][0][6:])
                if count != 0:
                    hoja = wb.create_sheet(name_sheet)
                    # wb.active = hoja
                else:
                    hoja = wb.active
                    hoja.title = name_sheet

                hoja.append(('FECHA', 'TIPO DE COMP.', 'N° COMPROB.', 'RAZON SOCIAL', 'FACTURADO (US$)', 'AMORITZADO (US$)', 'PENDIENTE(US$)', 'ESTADO', 'FECHA DE VENC.', 'CRÉDITO', 'DIAS DE VENC.', 'GUIAS', 'LETRAS', 'PAGOS')) # Crea la fila del encabezado con los títulos

                if global_sociedad == '2':
                    color_relleno = RELLENO_MP
                if global_sociedad == '1':
                    color_relleno = RELLENO_MC

                col_range = hoja.max_column  # get max columns in the worksheet
                # cabecera de la tabla
                for col in range(1, col_range + 1):
                    cell_header = hoja.cell(1, col)
                    cell_header.fill = color_relleno
                    cell_header.font = NEGRITA

                total_facturado_mes = 0
                for producto in info:
                    hoja.append(producto)
                    try:
                        total_facturado_mes += producto[4]
                    except Exception as e:
                        print(e)

                hoja.append(('','','','TOTAL:',total_facturado_mes))

                for row in hoja.rows:
                    for col in range(hoja.max_column):
                        row[col].border = BORDE_DELGADO
                        if 4 <= col <= 6:
                            row[col].alignment = ALINEACION_DERECHA
                            row[col].number_format = FORMATO_DOLAR
                        if col == 9 or col == 10:
                            row[col].alignment = ALINEACION_DERECHA
                        if 11 <= col <= 13:
                            row[col].alignment = AJUSTAR_TEXTO

                ajustarColumnasSheet(hoja)
                list = [name_sheet, total_facturado_mes] # Agregar mes en 0.00
                list_montos_totales.append(list)
                total_facturado += total_facturado_mes
                count += 1

            list_meses = [
                'ENERO',
                'FEBRERO',
                'MARZO',
                'ABRIL',
                'MAYO',
                'JUNIO',
                'JULIO',
                'AGOSTO',
                'SETIEMBRE',
                'OCTUBRE',
                'NOVIEMBRE',
                'DICIEMBRE'
                ]

            dict_meses_valor = {
                'ENERO' : 1,
                'FEBRERO': 2,
                'MARZO': 3,
                'ABRIL': 4,
                'MAYO': 5,
                'JUNIO': 6,
                'JULIO': 7,
                'AGOSTO': 8,
                'SETIEMBRE': 9,
                'OCTUBRE': 10,
                'NOVIEMBRE': 11,
                'DICIEMBRE' : 12,
            }

            # print()
            # print(list_montos_totales)
            # print()

            count = 0
            list_general = []
            list_temp = []
            for fila in list_montos_totales:
                if count != 0:
                    mes_resumen = fila[0].split(" - ")[0]
                    mes_anterior = list_montos_totales[count-1][0].split(" - ")[0]
                    if list_meses.index(mes_resumen) <= list_meses.index(mes_anterior):
                        list_general.append(list_temp)
                        list_temp = []
                list_temp.append(fila)
                count += 1
            list_general.append(list_temp)

            list_resumen_anuales = []
            for list_anual in list_general:
                list_temp_anual = []
                for fila in list_anual:
                    list_temp_anual.append(fila[0].split(" - ")[0])
                for mes_calendario in list_meses:
                    if mes_calendario not in list_temp_anual:
                        list_anual.insert(dict_meses_valor[mes_calendario]-1, [mes_calendario + " - " + fila[0].split(" - ")[1] , ])

                list_resumen_anuales += list_anual


            # print(13*' -- ')
            # print(list_general)
            # print()
            # print(list_resumen_anuales)
            # print()

            if global_sociedad == '2':
                color_relleno = RELLENO_MP
            if global_sociedad == '1':
                color_relleno = RELLENO_MC

            hoja = wb.create_sheet('Resumen')
            hoja.append(('ENERO', 'FEBRERO','MARZO','ABRIL','MAYO','JUNIO','JULIO','AGOSTO','SETIEMBRE','OCTUBRE','NOVIEMBRE','DICIEMBRE'))
            hoja.append(('', ''))
            hoja.append(('Periodo','Monto'))
            # for col in range(1, hoja.max_column + 1):
            for col in range(1, 2 + 1):
                cell_header = hoja.cell(3, col)
                cell_header.fill = color_relleno
                cell_header.font = NEGRITA

            for fila in list_resumen_anuales: # aqui! ANTES: "list_montos_totales"
                hoja.append(fila)
            # hoja.append(('TOTAL:',total_facturado)) # Es la sumatoria de todos los montos

            for row in hoja.rows:
                # for col in range(hoja.max_column):
                for col in range(2):
                    row[col].border = BORDE_DELGADO
                    if col == 1:
                        row[col].number_format = FORMATO_DOLAR
            ajustarColumnasSheet(hoja)


            # Insertar Gráfico

            def grafico_resumen_ingresos(ws):
                max_fila = ws.max_row - 3 # 3 filas de espacio antes de los meses

                chart = LineChart()
                # print(help(chart))
                chart.height = 15 # default is 7.5
                chart.width = 30 # default is 15
                chart.y_axis.title = 'VENTAS FACTURDAS'
                chart.x_axis.title = 'MESES'
                chart.legend.position = 'b' #bottom
                # chart.style = 12

                count = 1
                fila_base = 4
                year_base = int(ws['A' + str(fila_base)].value.split(' - ')[1]) - count # 2018
                data_col = 2 # montos en dolares
                if self.cod_soc == '1000':
                    chart.title = 'RESUMEN VENTAS FACTURADAS - MULTIPLAY'
                if self.cod_soc == '2000':
                    chart.title = 'RESUMEN VENTAS FACTURADAS - MULTICABLE'
                while max_fila >= 12:
                    values = Reference(ws, min_col = data_col, min_row = fila_base + 12*(count-1), max_col = data_col, max_row = 12*count + fila_base - 1)
                    # series = Series(values, title = "Ventas del " + str(year_base + count))
                    year_referencia = int(ws['A' + str(fila_base + 12*(count-1))].value.split(' - ')[1]) # 2018
                    series = Series(values, title = "Ventas del " + str(year_referencia))
                    chart.append(series)
                    max_fila -= 12
                    count += 1
                if 1 <= max_fila <= 12:
                    values = Reference(ws, min_col = data_col, min_row = fila_base + 12*(count-1), max_col = data_col, max_row = 12*count + fila_base - 1)
                    # series = Series(values, title = "Ventas del " + str(year_base + count))
                    year_referencia = int(ws['A' + str(fila_base + 12*(count-1))].value.split(' - ')[1]) # 2018
                    series = Series(values, title = "Ventas del " + str(year_referencia))
                    chart.append(series)

                meses = Reference(ws, min_col = 1, min_row = 1, max_col = 12, max_row = 1)
                chart.set_categories(meses)
                chart.dataLabels = DataLabelList()
                chart.dataLabels.showVal = True
                chart.dataLabels.dLblPos = 't' # top

                from openpyxl.chart.plotarea import DataTable
                chart.plot_area.dTable = DataTable()
                chart.plot_area.dTable.showHorzBorder = True
                chart.plot_area.dTable.showVertBorder = True
                chart.plot_area.dTable.showOutline = True
                chart.plot_area.dTable.showKeys = True

                ws.add_chart(chart)

            grafico_resumen_ingresos(hoja)


            return wb
            # wb.save('reporte_ventas_prueba.xlsx')

        # reporte_ventas('1000')

        wb=reporte_ventas()
        nombre_archivo = "Reporte_ventas_facturadas.xlsx"
        respuesta = HttpResponse(content_type='application/ms-excel')
        content = "attachment; filename ={0}".format(nombre_archivo)
        respuesta['content-disposition']= content
        wb.save(respuesta)
        return respuesta

class ReporteFacturasPendientes(TemplateView):
    def get(self,request, *args,**kwargs):
        global global_sociedad, global_fecha_inicio, global_fecha_fin

        def reporte_facturas_pendientes():
            wb = Workbook()
            hoja = wb.active

            if global_sociedad == '2':
                color_relleno = RELLENO_MP
            if global_sociedad == '1':
                color_relleno = RELLENO_MC

            sql_productos = ''' (SELECT
                    MAX(cvf.id) AS id,
                    to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                    'FACTURA' AS tipo_comprobante,
                    CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) AS nro_comprobante,
                    STRING_AGG(mm.descripcion_corta, ' | ') as productos
                    FROM comprobante_venta_facturaventa cvf
                    LEFT JOIN datos_globales_seriescomprobante dgsc
                        ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
                    LEFT JOIN comprobante_venta_facturaventadetalle cvfd
                        ON cvfd.factura_venta_id=cvf.id
                    LEFT JOIN material_material mm
                        ON cvfd.content_type_id='%s' AND mm.id=cvfd.id_registro
                    GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura)
                UNION
                (SELECT
                    MAX(cvb.id) AS id,
                    to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                    'BOLETA' AS tipo_comprobante,
                    CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT),6,'0')) AS nro_comprobante,
                    STRING_AGG(mm.descripcion_corta, ' | ') as productos
                    FROM comprobante_venta_boletaventa cvb
                    LEFT JOIN datos_globales_seriescomprobante dgsc
                        ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
                    LEFT JOIN comprobante_venta_boletaventadetalle cvbd
                        ON cvbd.boleta_venta_id=cvb.id
                    LEFT JOIN material_material mm
                        ON cvbd.content_type_id='%s' AND mm.id=cvbd.id_registro
                    GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta) ;'''%(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'],DICT_CONTENT_TYPE['material | material'],DICT_CONTENT_TYPE['comprobante_venta | boletaventa'],DICT_CONTENT_TYPE['material | material'],)
            query_info = FacturaVenta.objects.raw(sql_productos)

            info = []
            for fila in query_info:
                lista_datos = []
                lista_datos.append(fila.fecha_emision_comprobante)
                lista_datos.append(fila.tipo_comprobante)
                lista_datos.append(fila.nro_comprobante)
                lista_datos.append(fila.productos)
                info.append(lista_datos)

            dict_productos = {}
            for fila in info:
                dict_productos[fila[0]+'|'+fila[1]+'|'+fila[2]] = fila[3]

            # Letras según fechas pactadas al cotizar
            sql_letras = ''' (SELECT
                    MAX(cvf.id) AS id,
                    to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                    'FACTURA' AS tipo_comprobante,
                    CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) AS nro_comprobante,
                    MAX(cc.razon_social) AS cliente_denominacion,
                    (CASE WHEN MAX(cvf.tipo_venta)='2'
                    THEN (
                        STRING_AGG(CONCAT(
                            to_char(cobc.fecha, 'DD/MM/YYYY'),
                            ' $ ',
                            CAST(ROUND(cobc.monto,2) AS TEXT)
                            ), '\n' ORDER BY cobc.fecha)
                    ) ELSE (
                        ''
                    ) END) AS letras
                    FROM comprobante_venta_facturaventa cvf
                    LEFT JOIN datos_globales_seriescomprobante dgsc
                        ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
                    LEFT JOIN clientes_cliente cc
                        ON cc.id=cvf.cliente_id
                    LEFT JOIN cobranza_deuda cd
                        ON cd.content_type_id='%s' AND cd.id_registro=cvf.id
                    LEFT JOIN cobranza_cuota cobc
                        ON cobc.deuda_id=cd.id
                    WHERE cvf.tipo_venta='2' AND cvf.sociedad_id='%s' AND cd.id IS NOT NULL
                    GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura
                    ORDER BY cliente_denominacion ASC, letras ASC)
                UNION
                (SELECT
                    MAX(cvb.id) AS id,
                    to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                    'BOLETA' AS tipo_comprobante,
                    CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT),6,'0')) AS nro_comprobante,
                    MAX(cc.razon_social) AS cliente_denominacion,
                    (CASE WHEN MAX(cvb.tipo_venta)='2'
                    THEN (
                        STRING_AGG(CONCAT(
                            to_char(cobc.fecha, 'DD/MM/YYYY'),
                            ' $ ',
                            CAST(ROUND(cobc.monto,2) AS TEXT)
                            ), '\n' ORDER BY cobc.fecha)
                    ) ELSE (
                        ''
                    ) END) AS letras
                    FROM comprobante_venta_boletaventa cvb
                    LEFT JOIN datos_globales_seriescomprobante dgsc
                        ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
                    LEFT JOIN clientes_cliente cc
                        ON cc.id=cvb.cliente_id
                    LEFT JOIN cobranza_deuda cd
                        ON cd.content_type_id='%s' AND cd.id_registro=cvb.id
                    LEFT JOIN cobranza_cuota cobc
                        ON cobc.deuda_id=cd.id
                    WHERE cvb.tipo_venta='2' AND cvb.sociedad_id='%s' AND cd.id IS NOT NULL
                    GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta
                    ORDER BY cliente_denominacion ASC, letras ASC)
            ORDER BY cliente_denominacion ASC, letras ASC ; ''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'],DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], global_sociedad, DICT_CONTENT_TYPE['comprobante_venta | boletaventa'],DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], global_sociedad)
            query_info = FacturaVenta.objects.raw(sql_letras)

            info = []
            for fila in query_info:
                lista_datos = []
                lista_datos.append(fila.fecha_emision_comprobante)
                lista_datos.append(fila.tipo_comprobante)
                lista_datos.append(fila.nro_comprobante)
                lista_datos.append(fila.cliente_denominacion)
                lista_datos.append(fila.letras)
                info.append(lista_datos)

            dict_letras = {}
            for fila in info:
                dict_letras[fila[0]+'|'+fila[1]+'|'+fila[2]] = fila[4]

            sql = ''' (SELECT
                    MAX(cvf.id) AS id,
                    to_char(MAX(cvf.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                    'FACTURA' AS tipo_comprobante,
                    CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvf.numero_factura) AS TEXT),6,'0')) AS nro_comprobante,
                    MAX(cc.razon_social) AS cliente_denominacion,
                    MAX(cvf.total) AS monto_facturado,
                    SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) + SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_amortizado,
                    MAX(cvf.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_pendiente,
                    (CASE WHEN CAST(ROUND(MAX(cvf.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END), 2) AS TEXT)='0.00'
                        THEN (
                            'CANCELADO'
                        ) ELSE (
                            'PENDIENTE'
                        ) END) AS estado_cobranza,
                    to_char(MAX(cvf.fecha_vencimiento), 'DD/MM/YYYY') AS fecha_vencimiento_comprobante,
                    EXTRACT(DAY FROM MAX(cvf.fecha_vencimiento)) - EXTRACT(DAY FROM MAX(cvf.fecha_emision)) AS dias_credito,
                    MAX(cvf.fecha_vencimiento) AS dias_vencimiento,
                    '' AS observaciones,
                    '' AS letras,
                    '' AS productos
                    FROM comprobante_venta_facturaventa cvf
                    LEFT JOIN datos_globales_seriescomprobante dgsc
                        ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvf.serie_comprobante_id
                    LEFT JOIN clientes_cliente cc
                        ON cc.id=cvf.cliente_id
                    LEFT JOIN cobranza_deuda cd
                        ON cd.content_type_id='%s' AND cd.id_registro=cvf.id
                    LEFT JOIN cobranza_pago cp
                        ON cp.deuda_id=cd.id AND cp.content_type_id='%s'
                    LEFT JOIN cobranza_ingreso ci
                        ON ci.id=cp.id_registro
                    LEFT JOIN datos_globales_cuentabancariasociedad dgcb
                        ON dgcb.id=ci.cuenta_bancaria_id
                    LEFT JOIN datos_globales_moneda dgm
                        ON dgm.id=dgcb.moneda_id
                    LEFT JOIN cobranza_redondeo cr
                        ON cr.deuda_id=cd.id
                    WHERE cvf.sociedad_id='%s' AND cvf.estado='4' AND cd.id IS NOT NULL
                    GROUP BY cvf.sociedad_id, cvf.tipo_comprobante, cvf.serie_comprobante_id, cvf.numero_factura
                    HAVING (CASE WHEN CAST(ROUND(MAX(cvf.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END), 2) AS TEXT)='0.00'
                        THEN (
                            'CANCELADO'
                        ) ELSE (
                            'PENDIENTE'
                        ) END) = 'PENDIENTE'
                    ORDER BY cliente_denominacion ASC, nro_comprobante ASC)
                UNION
                (SELECT
                    MAX(cvb.id) AS id,
                    to_char(MAX(cvb.fecha_emision), 'DD/MM/YYYY') AS fecha_emision_comprobante,
                    'BOLETA' AS tipo_comprobante,
                    CONCAT(MAX(dgsc.serie), '-', lpad(CAST(MAX(cvb.numero_boleta) AS TEXT),6,'0')) AS nro_comprobante,
                    MAX(cc.razon_social) AS cliente_denominacion,
                    MAX(cvb.total) AS monto_facturado,
                    SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) + SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_amortizado,
                    MAX(cvb.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END) - SUM(CASE WHEN cr.monto IS NOT NULL THEN (cr.monto) ELSE 0.00 END) AS monto_pendiente,
                    (CASE WHEN CAST(ROUND(MAX(cvb.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END), 2) AS TEXT)='0.00'
                        THEN (
                            'CANCELADO'
                        ) ELSE (
                            'PENDIENTE'
                        ) END) AS estado_cobranza,
                    to_char(MAX(cvb.fecha_vencimiento), 'DD/MM/YYYY') AS fecha_vencimiento_comprobante,
                    EXTRACT(DAY FROM MAX(cvb.fecha_vencimiento)) - EXTRACT(DAY FROM MAX(cvb.fecha_emision)) AS dias_credito,
                    MAX(cvb.fecha_vencimiento) AS dias_vencimiento,
                    '' AS observaciones,
                    '' AS letras,
                    '' AS productos
                    FROM comprobante_venta_boletaventa cvb
                    LEFT JOIN datos_globales_seriescomprobante dgsc
                        ON dgsc.tipo_comprobante_id='%s' AND dgsc.id=cvb.serie_comprobante_id
                    LEFT JOIN clientes_cliente cc
                        ON cc.id=cvb.cliente_id
                    LEFT JOIN cobranza_deuda cd
                        ON cd.content_type_id='%s' AND cd.id_registro=cvb.id
                    LEFT JOIN cobranza_pago cp
                        ON cp.deuda_id=cd.id AND cp.content_type_id='%s'
                    LEFT JOIN cobranza_ingreso ci
                        ON ci.id=cp.id_registro
                    LEFT JOIN datos_globales_cuentabancariasociedad dgcb
                        ON dgcb.id=ci.cuenta_bancaria_id
                    LEFT JOIN datos_globales_moneda dgm
                        ON dgm.id=dgcb.moneda_id
                    LEFT JOIN cobranza_redondeo cr
                        ON cr.deuda_id=cd.id
                    WHERE cvb.sociedad_id='%s' AND cvb.estado='4' AND cd.id IS NOT NULL
                    GROUP BY cvb.sociedad_id, cvb.tipo_comprobante, cvb.serie_comprobante_id, cvb.numero_boleta
                    HAVING (CASE WHEN CAST(ROUND(MAX(cvb.total) - SUM(CASE WHEN dgm.abreviatura='PEN' THEN ROUND(cp.monto/cp.tipo_cambio,2) ELSE cp.monto END), 2) AS TEXT)='0.00'
                        THEN (
                            'CANCELADO'
                        ) ELSE (
                            'PENDIENTE'
                        ) END) = 'PENDIENTE'
                    ORDER BY cliente_denominacion ASC, nro_comprobante ASC)
            ORDER BY cliente_denominacion ASC, nro_comprobante ASC ''' %(DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['comprobante_venta | facturaventa'], DICT_CONTENT_TYPE['cobranza | ingreso'], global_sociedad, DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['comprobante_venta | boletaventa'], DICT_CONTENT_TYPE['cobranza | ingreso'], global_sociedad)
            query_info = FacturaVenta.objects.raw(sql)

            info = []
            for fila in query_info:
                lista_datos = []
                lista_datos.append(fila.fecha_emision_comprobante)
                lista_datos.append(fila.tipo_comprobante)
                lista_datos.append(fila.nro_comprobante)
                lista_datos.append(fila.cliente_denominacion)
                lista_datos.append(fila.monto_facturado)
                lista_datos.append(fila.monto_amortizado)
                lista_datos.append(fila.monto_pendiente)
                lista_datos.append(fila.estado_cobranza)
                lista_datos.append(fila.fecha_vencimiento_comprobante)
                lista_datos.append(fila.dias_credito)
                lista_datos.append(str(fila.dias_vencimiento))
                lista_datos.append(fila.observaciones)
                lista_datos.append(fila.letras)
                lista_datos.append(fila.productos)
                info.append(lista_datos)

            dias = 0
            for fila in info:
                fila[4] = float(fila[4])
                if fila[5] == None:
                    fila[5] = '0.00'
                if fila[6] == None:
                    fila[6] = '0.00'
                fila[5] = float(fila[5])
                fila[6] = float(fila[6])
                fila[9] = float(fila[9])
                if fila[10] != '':
                    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
                    fecha1 = datetime.strptime(fecha_hoy, '%Y-%m-%d')
                    fecha2 = datetime.strptime(fila[10], '%Y-%m-%d')
                    dias = (fecha1 - fecha2) / timedelta(days=1)
                    fila[10] = str(dias)
                if float(dias) > float(0):
                    fila[7] = 'VENCIDO'
                if fila[0]+'|'+fila[1]+'|'+fila[2] in dict_letras:
                    fila[12] = dict_letras[fila[0]+'|'+fila[1]+'|'+fila[2]]
                else:
                    'ERROR AL EXTRAER LAS CUOTAS'
                fila[13] = dict_productos[fila[0]+'|'+fila[1]+'|'+fila[2]]

            num_fila = 0
            total_deuda_cliente = 0
            for fila in info:
                if num_fila != 0:
                    if fila[3] != info[num_fila-1][3]:
                        hoja.append(('','','','Total:',float(total_deuda_cliente)))
                        # cell_total = hoja.cell(hoja.max_row, 4)
                        # cell_total.alignment = self.alineacion_derecha
                        # cell_total.number_format = self.formato_dolar
                        hoja.append(('',))
                        hoja.append((fila[3],))
                        hoja.append(('FECHA','N° COMPROBANTE','FACTURADO (US$)','AMORTIZADO','PENDIENTE','ESTADO','FECHA DE VENC.','CRÉDITO (DÍAS)','DÍAS DE VENC.','OBSERVACIONES','LETRAS','PRODUCTOS'))
                        total_deuda_cliente = 0
                        col_range = hoja.max_column
                        nueva_fila = hoja.max_row
                        for col in range(1, col_range + 1):
                            cell_header = hoja.cell(nueva_fila, col)
                            cell_header.fill = color_relleno
                            cell_header.font = NEGRITA
                else:
                    hoja.append((fila[3],))
                    hoja.append(('FECHA','N° COMPROBANTE','FACTURADO (US$)','AMORTIZADO','PENDIENTE','ESTADO','FECHA DE VENC.','CRÉDITO (DÍAS)','DÍAS DE VENC.','OBSERVACIONES','LETRAS','PRODUCTOS'))
                    col_range = hoja.max_column
                    nueva_fila = hoja.max_row
                    for col in range(1, col_range + 1):
                        cell_header = hoja.cell(nueva_fila, col)
                        cell_header.fill = color_relleno
                        cell_header.font = NEGRITA

                c = 0
                list_temp = []
                for dato in fila:
                    if c != 1 and c != 3: # tipo_comprobante, razon_social (datos omitidos en la tabla)
                        list_temp.append(dato)
                    c+=1

                hoja.append(list_temp)
                total_deuda_cliente += list_temp[4]
                num_fila += 1

                for i in range(hoja.max_row):
                    if i >= nueva_fila-1:
                        row = list(hoja.rows)[i]
                        for col in range(hoja.max_column):
                            row[col].border = BORDE_DELGADO
                            if 2 <= col <= 4:
                                row[col].alignment = ALINEACION_DERECHA
                                row[col].number_format = FORMATO_DOLAR
                            if col == 7 or col == 8:
                                row[col].alignment = ALINEACION_DERECHA
                            if 10 <= col <= 11:
                                row[col].alignment = AJUSTAR_TEXTO

                if fila == info[-1]:
                    hoja.append(('','','','Total:',float(total_deuda_cliente)))
                    # cell_total = hoja.cell(hoja.max_row, 4)
                    # cell_total.alignment = self.alineacion_derecha
                    # cell_total.number_format = self.formato_dolar

            ajustarColumnasSheet(hoja)
            return wb
            # wb.save('reporte4_prueba.xlsx')


        # reporte_facturas_pendientes('2000')
        query_sociedad = Sociedad.objects.filter(id = int(global_sociedad))[0]
        abreviatura = query_sociedad.abreviatura
        wb=reporte_facturas_pendientes()
        nombre_archivo = "Reporte_facturas_pendientes - " + abreviatura + " - " + FECHA_HOY + ".xlsx"
        respuesta = HttpResponse(content_type='application/ms-excel')
        content = "attachment; filename ={0}".format(nombre_archivo)
        respuesta['content-disposition']= content
        wb.save(respuesta)
        return respuesta