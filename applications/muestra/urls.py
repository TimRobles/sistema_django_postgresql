from django.urls import path
from . import views

app_name = 'muestra_app'

urlpatterns = [
    path('nota-ingreso-muestra/crear/', views.NotaIngresoMuestraCreateView.as_view(), name='nota_ingreso_muestra_crear'),
    path('nota-ingreso-muestra/eliminar/<pk>/', views.NotaIngresoMuestraEliminarView.as_view(), name='nota_ingreso_muestra_eliminar'),
    path('nota-ingreso-muestra/lista/', views.NotaIngresoMuestraListaView.as_view(), name='nota_ingreso_muestra_lista_total'),
    path('nota-ingreso-muestra/detalle/<pk>/', views.NotaIngresoMuestraDetailView.as_view(), name='nota_ingreso_muestra_detalle'),
    path('nota-ingreso-muestra/detalle/tabla/<pk>/', views.NotaIngresoMuestraDetailTabla, name='nota_ingreso_muestra_detalle_tabla'),
    path('nota-ingreso-muestra/agregar-material/<int:id_nota_ingreso_muestra>/', views.NotaIngresoMuestraAgregarMaterialView.as_view(), name='nota_ingreso_muestra_agregar_material'),
    path('nota-ingreso-muestra/actualizar-material/<int:id_nota_ingreso_muestra_detalle>/', views.NotaIngresoMuestraActualizarMaterialView.as_view(), name='nota_ingreso_muestra_actualizar_material'),
    path('nota-ingreso-muestra/eliminar-material/<pk>/', views.NotaIngresoMuestraDetalleEliminarView.as_view(), name='nota_ingreso_muestra_eliminar_material'),
    path('nota-ingreso-muestra/guardar/<pk>/', views.NotaIngresoMuestraGuardarView.as_view(), name='nota_ingreso_muestra_guardar'),
    path('nota-ingreso-muestra/anular/<pk>/', views.NotaIngresoMuestraAnularView.as_view(), name='nota_ingreso_muestra_anular'),

    path('validar-series/nota-ingreso-muestra/detalle/<pk>/', views.ValidarSeriesNotaIngresoMuestraDetailView.as_view(), name='validar_series_nota_ingreso_muestra_detalle'),
    path('validar-series/nota-ingreso-muestra/detalle-tabla/<pk>/', views.ValidarSeriesNotaIngresoMuestraDetailTabla, name='validar_series_nota_ingreso_muestra_detalle_tabla'),
    path('validar-series-detalle/nota-ingreso-muestra/eliminar/<pk>/', views.ValidarSeriesNotaIngresoMuestraDetalleDeleteView.as_view(), name='validar_series_nota_ingreso_muestra_detalle_eliminar'),
    
]