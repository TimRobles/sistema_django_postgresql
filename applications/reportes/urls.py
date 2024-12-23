from django.urls import path
from . import views

app_name = 'reportes_app'

urlpatterns = [ 

    path('reportes/', views.ReportesView.as_view(), name='reportes_inicio'),
    path('reporte-contador/', views.ReporteContador.as_view(), name='reporte_contador'),
    path('reporte-ventas-facturadas/', views.ReporteVentasFacturadas.as_view(), name='reporte_ventas_facturadas'),
    path('reporte-facturas-pendientes/', views.ReporteFacturasPendientes.as_view(), name='reporte_facturas_pendientes'),
    path('reporte-depositos-cuentas-bancarias/', views.ReporteDepositosCuentasBancarias.as_view(), name='reporte_depositos_cuentas_bancarias'),
    path('reporte-clientes-productos/', views.ReporteClientesProductos.as_view(), name='reporte_clientes_productos'),
    path('reporte-deudas/', views.ReporteDeudas.as_view(), name='reporte_deudas'),
    path('reporte-cobranza/', views.ReporteCobranza.as_view(), name='reporte_cobranza'),
    path('reporte-rotacion/', views.ReporteRotacion.as_view(), name='reporte_rotacion'),
    path('reporte-resumen-stock-productos-excel/', views.ReporteResumenStockProductosExcel.as_view(), name='reporte_resumen_stock_productos_excel'),
    path('reporte-resumen-stock-productos-pdf/', views.ReporteResumenStockProductosPDF.as_view(), name='reporte_resumen_stock_productos_pdf'),
    path('reporte-stock-sociedad-pdf/', views.ReportesCorregidosPdf.as_view(), name='reporte_stock_sociedad_pdf'),
    path('reportes-crm-excel/', views.ReportesCRM.as_view(), name='reportes_crm_excel'),
    path('reportes-gerencia-excel/', views.ReportesGerencia.as_view(), name='reportes_gerencia_excel'),
    path('reportes-corregidos/', views.ReportesCorregidosExcel.as_view(), name='reportes_corregidos'),
    path('reportes-producto-precioventa-pdf/', views.ReporteProductoPorPrecioVentaPDF.as_view(), name='reportes_producto_precioventa_pdf'),
    path('reportes-producto-precioventa-pdf/', views.ReporteProductoPorPrecioVentaPDF.as_view(), name='reportes_producto_precioventa_pdf'),
 ]