from django.shortcuts import render
from applications.importaciones import *
from applications.reportes_panel.forms import ReportesPanelFiltrosForm
from applications.material.forms import Material
from applications.reportes.funciones import *
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Alignment
from openpyxl.styles import *
from openpyxl.styles.borders import Border, Side
from openpyxl.chart import Reference, Series,LineChart
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.plotarea import DataTable

def mostrar_info_tabla(filtro_sociedad, filtro_marca, filtro_fecha_inicio, filtro_fecha_fin):
    sql_base = '''SELECT
            MAX(mm.id) as id,
            MAX(mm.descripcion_corta) as material_texto,
            ROUND(SUM(mam.cantidad*mam.signo_factor_multiplicador),2) as total_stock
        FROM movimiento_almacen_movimientosalmacen mam
        LEFT JOIN material_material mm
            ON mm.id=mam.id_registro_producto AND mam.content_type_producto_id='52'
        LEFT JOIN movimiento_almacen_tipostock mats
            ON mam.tipo_stock_id=mats.id
        WHERE mats.codigo NOT IN (
            1, 2, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25) '''
    sql_where_marca = '''AND mm.marca_id='%s' ''' %(filtro_marca) if filtro_marca else ''
    sql_final = ''' GROUP BY mm.id ORDER BY mm.descripcion_corta ; '''
    sql_stock = sql_base + sql_where_marca + sql_final
    query_info = Material.objects.raw(sql_stock)
    dict_stock = {}
    for fila in query_info:
        dict_stock[fila.id] = fila.total_stock
        
    sql_base = ''' SELECT 
            MAX(mm.id) AS id,
            MAX(mma.nombre) AS descrip_marca,
            MAX(mm.descripcion_corta) AS material_texto,
            ROUND(SUM(cvfd.cantidad),2) AS venta_total,
            MIN(cvf.fecha_emision) AS primera_venta,
            MAX(cvf.fecha_emision) AS ultima_venta,
            COUNT(cvf.id) AS nro_ventas,
            '' AS stock_total
        FROM material_material mm
        LEFT JOIN material_marca mma
            ON mm.marca_id=mma.id
        LEFT JOIN comprobante_venta_facturaventadetalle cvfd
            ON cvfd.content_type_id='52' AND mm.id=cvfd.id_registro
        LEFT JOIN comprobante_venta_facturaventa cvf
            ON cvf.id=cvfd.factura_venta_id
        LEFT JOIN sociedad_sociedad ss
            ON ss.id=cvf.sociedad_id
        WHERE (cvf.estado='4' OR cvf.estado IS NULL) '''
    sql_where_sociedad = '''AND (cvf.sociedad_id IS NULL OR cvf.sociedad_id='%s') ''' %(filtro_sociedad) if filtro_sociedad else ''
    sql_where_marca = '''AND mm.marca_id='%s' ''' %(filtro_marca) if filtro_marca else ''
    sql_where_fechainicio = '''AND cvf.fecha_emision>='%s' ''' %(filtro_fecha_inicio) if filtro_fecha_inicio else ''
    sql_where_fechafin = '''AND cvf.fecha_emision<='%s' ''' %(filtro_fecha_fin) if filtro_fecha_fin else ''
    sql_final = '''GROUP BY mm.id ORDER BY 3 ; '''
    sql_1 = sql_base + sql_where_sociedad + sql_where_marca + sql_where_fechainicio + sql_where_fechafin + sql_final
    
    query_info = Material.objects.raw(sql_1)
    list_info_facturas = []
    dict_info_facturas = {}
    for fila in query_info:
        list_temp = []
        stock_total = dict_stock[fila.id] if fila.id in dict_stock else 0.00
        venta_total = float(fila.venta_total) if fila.venta_total else float(0.00)
        ultima_venta = fila.ultima_venta if fila.ultima_venta else '--'
        list_temp.extend([
            fila.descrip_marca,
            fila.material_texto,
            venta_total,
            ultima_venta,
            stock_total
            ])
        dict_info_facturas[fila.id] = list_temp
        list_info_facturas.append(list_temp)

    sql_base = ''' SELECT 
            MAX(mm.id) AS id,
            MAX(mma.nombre) AS descrip_marca,
            MAX(mm.descripcion_corta) AS material_texto,
            ROUND(SUM(cvbd.cantidad),2) AS venta_total,
            MIN(cvb.fecha_emision) AS primera_venta,
            MAX(cvb.fecha_emision) AS ultima_venta,
            COUNT(cvb.id) AS nro_ventas,
            '' AS stock_total
        FROM material_material mm
        LEFT JOIN material_marca mma
            ON mm.marca_id=mma.id
        LEFT JOIN comprobante_venta_boletaventadetalle cvbd
            ON cvbd.content_type_id='52' AND mm.id=cvbd.id_registro
        LEFT JOIN comprobante_venta_boletaventa cvb
            ON cvb.id=cvbd.boleta_venta_id
        LEFT JOIN sociedad_sociedad ss
            ON ss.id=cvb.sociedad_id
        WHERE (cvb.estado='4' OR cvb.estado IS NULL) '''
    sql_where_sociedad = '''AND (cvb.sociedad_id IS NULL OR cvb.sociedad_id='%s') ''' %(filtro_sociedad) if filtro_sociedad else ''
    sql_where_marca = '''AND mm.marca_id='%s' ''' %(filtro_marca) if filtro_marca else ''
    sql_where_fechainicio = '''AND cvb.fecha_emision>='%s' ''' %(filtro_fecha_inicio) if filtro_fecha_inicio else ''
    sql_where_fechafin = '''AND cvb.fecha_emision<='%s' ''' %(filtro_fecha_fin) if filtro_fecha_fin else ''
    sql_final = '''GROUP BY mm.id ORDER BY 3 ; '''
    sql_2 = sql_base + sql_where_sociedad + sql_where_marca + sql_where_fechainicio + sql_where_fechafin + sql_final

    # sql = sql_1 + sql_2
    query_info = Material.objects.raw(sql_2)
    list_info_boletas = []
    for fila in query_info:
        list_temp = []
        stock_total = dict_stock[fila.id] if fila.id in dict_stock else 0.00
        venta_total = float(fila.venta_total) if fila.venta_total else float(0.00)
        ultima_venta = fila.ultima_venta if fila.ultima_venta else '--'
        list_temp.extend([
            fila.descrip_marca,
            fila.material_texto,
            venta_total,
            ultima_venta,
            stock_total
            ])
        if fila.id in dict_info_facturas:
            dict_info_facturas[fila.id][2] += venta_total
            if dict_info_facturas[fila.id][3] == '--':
                dict_info_facturas[fila.id][3] = ultima_venta
            elif ultima_venta != '--':
                if dict_info_facturas[fila.id][3] < ultima_venta:
                    dict_info_facturas[fila.id][3] = ultima_venta
        else:
            dict_info_facturas[fila.id] = list_temp
        list_info_boletas.append(list_temp)

    list_info = dict_info_facturas.values()
    return list_info


class MarcaVentasListView(ListView):
    model = Material
    template_name = "reportes_panel/marca_ventas/inicio.html"
    context_object_name = 'contexto_marca_ventas'
    # def get_queryset(self):
    #     consulta = super().get_queryset()
    #     return consulta.filter(mostrar=1)

    def get_context_data(self, **kwargs):
        context = super(MarcaVentasListView, self).get_context_data(**kwargs)
        query_active = True
        if query_active:
            sql = ''' SELECT 
                    MAX(mm.id) AS id,
                    MAX(mm.descripcion_corta) AS material_texto,
                    ROUND(SUM(cvfd.cantidad),2) AS venta_total,
                    MIN(cvf.fecha_emision) AS primera_venta,
                    MAX(cvf.fecha_emision) AS ultima_venta,
                    COUNT(cvf.id) AS nro_ventas
                FROM material_material mm
                LEFT JOIN comprobante_venta_facturaventadetalle cvfd
                    ON cvfd.content_type_id='52' AND mm.id=cvfd.id_registro
                LEFT JOIN comprobante_venta_facturaventa cvf
                    ON cvf.id=cvfd.factura_venta_id
                WHERE (cvf.estado='4' or cvf.estado is NULL) AND mm.marca_id='15'
                GROUP BY mm.id
                ORDER BY mm.descripcion_corta; '''
            query_context = Material.objects.raw(sql)
            context['contexto_marca_ventas'] = query_context
        
        else:
            query_context = Material.objects.all()
            context['contexto_marca_ventas'] = query_context
        return context


class ReportesMarcaVentasView(FormView):
    template_name = "reportes_panel/marca_ventas/inicio.html"
    form_class = ReportesPanelFiltrosForm
    success_url = '.' 

    def get_form_kwargs(self):
        kwargs = super(ReportesMarcaVentasView, self).get_form_kwargs()
        kwargs['filtro_marca'] = self.request.GET.get('marca')
        kwargs['filtro_sociedad'] = self.request.GET.get('sociedad')
        kwargs['filtro_fecha_inicio'] = self.request.GET.get('fecha_inicio')
        kwargs['filtro_fecha_fin'] = self.request.GET.get('fecha_fin')
        # kwargs['filtro_cliente'] = self.request.GET.get('cliente')
        global global_sociedad, global_fecha_inicio, global_fecha_fin, global_marca
        global_marca = self.request.GET.get('marca')
        global_sociedad = self.request.GET.get('sociedad')
        global_fecha_inicio = self.request.GET.get('fecha_inicio')
        global_fecha_fin = self.request.GET.get('fecha_fin')
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super(ReportesMarcaVentasView, self).get_context_data(**kwargs)
        contexto_filtros = []
        filtro_marca = self.request.GET.get('marca')
        filtro_sociedad = self.request.GET.get('sociedad')
        filtro_fecha_inicio = self.request.GET.get('fecha_inicio')
        filtro_fecha_fin = self.request.GET.get('fecha_fin')
        # filtro_cliente = self.request.GET.get('cliente')
        contexto_filtros.append(f"filtro_marca={filtro_marca}")
        contexto_filtros.append(f"filtro_sociedad={filtro_sociedad}")
        contexto_filtros.append(f"filtro_fecha_inicio={filtro_fecha_inicio}")
        contexto_filtros.append(f"filtro_fecha_fin={filtro_fecha_fin}")
        # contexto_filtros.append(f"filtro_cliente={filtro_cliente}")
        context["contexto_filtros"] = "&".join(contexto_filtros)
        context['contexto_marca_ventas'] = mostrar_info_tabla(filtro_sociedad, filtro_marca, filtro_fecha_inicio, filtro_fecha_fin)
        return context


class ReportesPanelTemplateView(TemplateView):
    template_name = "reportes_panel/inicio.html"
    

# class MarcaVentasListView(PermissionRequiredMixin, ListView):
    # permission_required = ('material.view_marca')


class ReporteExcelMarcaVentas(TemplateView):

    def get(self, request, *args,**kwargs):
        filtro_marca = self.request.GET.get('filtro_marca')
        filtro_sociedad = self.request.GET.get('filtro_sociedad')
        filtro_fecha_inicio = self.request.GET.get('filtro_fecha_inicio')
        filtro_fecha_fin = self.request.GET.get('filtro_fecha_fin')

        def reporte_marca_ventas():
            wb = Workbook()
            hoja = wb.active
            hoja.title = 'MARCA VS VENTAS'

            hoja.append(('MARCA', 'DESCRIPCIÓN', 'TOTAL VENDIDO', 'FECHA ÚLTIMA VENTA', 'STOCK'))

            color_relleno = rellenoSociedad(filtro_sociedad)

            col_range = hoja.max_column
            for col in range(1, col_range + 1):
                cell_header = hoja.cell(1, col)
                cell_header.fill = color_relleno
                cell_header.font = NEGRITA

            info = mostrar_info_tabla(filtro_sociedad, filtro_marca, filtro_fecha_inicio, filtro_fecha_fin)
            for producto in info:
                hoja.append(producto)

            for row in hoja.rows:
                for col in range(hoja.max_column):
                    row[col].border = BORDE_DELGADO

            ajustarColumnasSheet(hoja)
            return wb

        if filtro_sociedad:
            query_sociedad = Sociedad.objects.filter(id = int(filtro_sociedad))[0]
            abreviatura = query_sociedad.abreviatura
        else:
            abreviatura = 'MPL-MCA'
        wb = reporte_marca_ventas()
        nombre_archivo = "Reporte Marca vs Ventas - " + abreviatura + " - " + FECHA_HOY + ".xlsx"
        respuesta = HttpResponse(content_type='application/ms-excel')
        content = "attachment; filename ={0}".format(nombre_archivo)
        respuesta['content-disposition']= content
        wb.save(respuesta)
        return respuesta
