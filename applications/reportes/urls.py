from django.urls import path
from . import views

app_name = 'reportes_app'

reportes_crm = [
    path('reportes-crm/', views.ReportesCRMView.as_view(), name='reportes_crm_inicio'),
    path('reportes-crm/cliente-crm/', views.ReporteClienteCRM.as_view(), name='reporte_cliente_crm'),
    path('reportes-crm/facturacion-anual/', views.ReporteFacturacionAnual.as_view(), name='reporte_facturacion_anual'),
    # path('reportes-crm/facturacion-periodos/', views.ReporteFacturacionPeriodos.as_view(), name='reporte_facturacion_periodos'),
    # path('reportes-crm/encuestas/', views.ReporteEncuestas.as_view(), name='reporte_encuestas'),
    # path('reportes-crm/comportamiento/', views.ReporteComportamiento.as_view(), name='reporte_comportamiento'),
    # path('reportes-crm/clientes-nuevos-finales/', views.ReporteClientesNuevosFinales.as_view(), name='reporte_clientes_nuevos_finales'),
    # path('reportes-crm/asesor-ventas/', views.ReporteAsesorVentas.as_view(), name='reporte_asesor_ventas'),
    # path('reportes-crm/clientes-medios/', views.ReporteClientesMedios.as_view(), name='reporte_clientes_medios'),
    # path('reportes-crm/facturacion-ubigeo/', views.ReporteFacturacionUbigeo.as_view(), name='reporte_facturacion_ubigeo'),

]

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
    path('reporte-stock-sociedad-pdf/', views.ReporteStockSociedadPdf.as_view(), name='reporte_stock_sociedad_pdf'),
 ] + reportes_crm