from django.urls import path
from . import views

app_name = 'nota_ingreso_app'

urlpatterns = [
    path('nota-ingreso/lista/<int:recepcion_id>/', views.NotaIngresoView.as_view(), name='nota_ingreso_lista'),
    path('nota-ingreso/detalle/<pk>/', views.NotaIngresoDetailView.as_view(), name='nota_ingreso_detalle'),
    path('nota-ingreso/detalle/tabla/<int:recepcion_id>/', views.NotaIngresoDetailTabla, name='nota_ingreso_detalle_tabla'),
    path('nota-ingreso/agregar-material/<int:id_nota_ingreso>/', views.NotaIngresoAgregarMaterialView.as_view(), name='nota_ingreso_agregar_material'),
    path('nota-ingreso/actualizar-material/<int:id_nota_ingreso_detalle>/', views.NotaIngresoActualizarMaterialView.as_view(), name='nota_ingreso_actualizar_material'),
    path('nota-ingreso/eliminar-material/<pk>/', views.NotaIngresoDetalleEliminarView.as_view(), name='nota_ingreso_eliminar_material'),
    path('nota-ingreso/finalizar-conteo/<pk>/', views.NotaIngresoFinalizarConteoView.as_view(), name='nota_ingreso_finalizar_conteo'),

]