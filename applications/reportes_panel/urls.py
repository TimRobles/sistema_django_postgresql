from django.urls import path
from .views import ReportesPanelTemplateView, ReportesMarcaVentasView, ReporteExcelMarcaVentas, ProductoClienteVentasView, ProductoClienteVentasDetalle, UbigeoVentasView

app_name = 'reportes_panel_app'

urlpatterns = [
    path('', ReportesPanelTemplateView.as_view(), name='reportes_panel_inicio'),
    path('reportes_panel_marcasventa/', ReportesMarcaVentasView.as_view(), name='reportes_panel_marcasventa'),
    path('reportes_panel_marcasventa_descargar/', ReporteExcelMarcaVentas.as_view(), name='reportes_panel_marcasventa_descargar'),
    path('reportes_panel_productoclienteventas/', ProductoClienteVentasView.as_view(), name='reportes_panel_productoclienteventas'),
    path('reportes_panel_productoclienteventas_detalle/<pk>', ProductoClienteVentasDetalle.as_view(), name='reportes_panel_productoclienteventas_detalle'),
    path('reportes_panel_ubigeoventas/', UbigeoVentasView.as_view(), name='reportes_panel_ubigeoventas')
]
