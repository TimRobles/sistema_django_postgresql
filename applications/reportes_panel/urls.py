from django.urls import path
from . import views

app_name = 'reportes_panel_app'

urlpatterns = [
    path('', views.ReportesPanelTemplateView.as_view(), name='reportes_panel_inicio'),
    path('reportes_panel_marcasventa/', views.ReportesMarcaVentasView.as_view(), name='reportes_panel_marcasventa'),
    path('reportes_panel_marcasventa_descargar/', views.ReporteExcelMarcaVentas.as_view(), name='reportes_panel_marcasventa_descargar'),
]
