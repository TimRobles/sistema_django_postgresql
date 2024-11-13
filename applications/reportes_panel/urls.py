from django.urls import path
from .views import (
    ReportesPanelTemplateView, 
    ReportesMarcaVentasView, 
    ReporteExcelMarcaVentas, 
    ProductoClienteVentasView, 
    ProductoClienteVentasDetalle, 
    UbigeoVentasView)

app_name = 'reportes_panel_app'

urlpatterns = [
    path('', ReportesPanelTemplateView.as_view(), name='reportes_panel_inicio'),
    path('marcas-venta/', ReportesMarcaVentasView.as_view(), name='reportes_panel_marcasventa'),
    path('marcas-venta-descargar/', ReporteExcelMarcaVentas.as_view(), name='reportes_panel_marcasventa_descargar'),
    path('producto-cliente-ventas/', ProductoClienteVentasView.as_view(), name='reportes_panel_productoclienteventas'),
    path('producto-cliente-ventas-detalle/<pk>', ProductoClienteVentasDetalle.as_view(), name='reportes_panel_productoclienteventas_detalle'),
    path('ubigeo-ventas/', UbigeoVentasView.as_view(), name='reportes_panel_ubigeoventas'),
]
