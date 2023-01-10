from django.urls import path
from . import views

app_name = 'reportes_app'

urlpatterns = [ 

    path('reportes/', views.ReportesView.as_view(), name='reportes_inicio'),
    path('reporte-contador/', views.ReporteContador.as_view(), name='reporte_contador'),
    path('reporte-ventas-facturadas/', views.ReporteVentasFacturadas.as_view(), name='reporte_ventas_facturadas'),
    path('reporte-facturas-pendientes/', views.ReporteFacturasPendientes.as_view(), name='reporte_facturas_pendientes'),
 ]