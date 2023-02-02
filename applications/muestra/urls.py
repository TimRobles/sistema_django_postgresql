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

    path('nota-ingreso-muestra/generar-nota-ingreso/<int:pk>/', views.NotaIngresoMuestraGenerarNotaIngresoView.as_view(), name='nota_ingreso_muestra_generar_nota_ingreso'),

    path('devolucion-muestra/crear/', views.DevolucionMuestraCreateView.as_view(), name='devolucion_muestra_crear'),
    path('devolucion-muestra/eliminar/<pk>/', views.DevolucionMuestraEliminarView.as_view(), name='devolucion_muestra_eliminar'),
    path('devolucion-muestra/lista/', views.DevolucionMuestraListaView.as_view(), name='devolucion_muestra_lista_total'),
    path('devolucion-muestra/detalle/<pk>/', views.DevolucionMuestraDetailView.as_view(), name='devolucion_muestra_detalle'),
    path('devolucion-muestra/detalle/tabla/<pk>/', views.DevolucionMuestraDetailTabla, name='devolucion_muestra_detalle_tabla'),
    path('devolucion-muestra/agregar-material/<int:id_devolucion_muestra>/', views.DevolucionMuestraAgregarMaterialView.as_view(), name='devolucion_muestra_agregar_material'),
    path('devolucion-muestra/actualizar-material/<int:id_devolucion_muestra_detalle>/', views.DevolucionMuestraActualizarMaterialView.as_view(), name='devolucion_muestra_actualizar_material'),
    path('devolucion-muestra/eliminar-material/<pk>/', views.DevolucionMuestraDetalleEliminarView.as_view(), name='devolucion_muestra_eliminar_material'),
    path('devolucion-muestra/guardar/<pk>/', views.DevolucionMuestraGuardarView.as_view(), name='devolucion_muestra_guardar'),
    path('devolucion-muestra/anular/<pk>/', views.DevolucionMuestraAnularView.as_view(), name='devolucion_muestra_anular'),

    path('devolucion-muestra/generar-guia/<pk>/', views.DevolucionMuestraGenerarGuiaView.as_view(), name='devolucion_muestra_generar_guia'),
]