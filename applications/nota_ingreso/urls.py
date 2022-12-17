from django.urls import path
from . import views

app_name = 'nota_ingreso_app'

urlpatterns = [
    path('nota-ingreso/lista/<int:recepcion_id>/', views.NotaIngresoView.as_view(), name='nota_ingreso_lista'),
    path('nota-ingreso/lista/nota-stock-inicial/<int:nota_stock_inicial_id>/', views.NotaIngresoNotaStockInicialView.as_view(), name='nota_ingreso_lista_nota_stock_inicial'),
    path('nota-ingreso/lista/', views.NotaIngresoListaView.as_view(), name='nota_ingreso_lista_total'),
    path('nota-ingreso/detalle/<pk>/', views.NotaIngresoDetailView.as_view(), name='nota_ingreso_detalle'),
    path('nota-ingreso/detalle/tabla/<int:recepcion_id>/', views.NotaIngresoDetailTabla, name='nota_ingreso_detalle_tabla'),
    path('nota-ingreso/agregar-material/<int:id_nota_ingreso>/', views.NotaIngresoAgregarMaterialView.as_view(), name='nota_ingreso_agregar_material'),
    path('nota-ingreso/actualizar-material/<int:id_nota_ingreso_detalle>/', views.NotaIngresoActualizarMaterialView.as_view(), name='nota_ingreso_actualizar_material'),
    path('nota-ingreso/eliminar-material/<pk>/', views.NotaIngresoDetalleEliminarView.as_view(), name='nota_ingreso_eliminar_material'),
    path('nota-ingreso/finalizar-conteo/<pk>/', views.NotaIngresoFinalizarConteoView.as_view(), name='nota_ingreso_finalizar_conteo'),
    path('nota-ingreso/anular-conteo/<pk>/', views.NotaIngresoAnularConteoView.as_view(), name='nota_ingreso_anular_conteo'),

    path('nota-stock-inicial/crear/', views.NotaStockInicialCreateView.as_view(), name='nota_stock_inicial_crear'),
    path('nota-stock-inicial/eliminar/<pk>/', views.NotaStockInicialEliminarView.as_view(), name='nota_stock_inicial_eliminar'),
    path('nota-stock-inicial/lista/', views.NotaStockInicialListaView.as_view(), name='nota_stock_inicial_lista_total'),
    path('nota-stock-inicial/detalle/<pk>/', views.NotaStockInicialDetailView.as_view(), name='nota_stock_inicial_detalle'),
    path('nota-stock-inicial/detalle/tabla/<pk>/', views.NotaStockInicialDetailTabla, name='nota_stock_inicial_detalle_tabla'),
    path('nota-stock-inicial/agregar-material/<int:id_nota_stock_inicial>/', views.NotaStockInicialAgregarMaterialView.as_view(), name='nota_stock_inicial_agregar_material'),
    path('nota-stock-inicial/actualizar-material/<int:id_nota_stock_inicial_detalle>/', views.NotaStockInicialActualizarMaterialView.as_view(), name='nota_stock_inicial_actualizar_material'),
    path('nota-stock-inicial/eliminar-material/<pk>/', views.NotaStockInicialDetalleEliminarView.as_view(), name='nota_stock_inicial_eliminar_material'),
    path('nota-stock-inicial/guardar/<pk>/', views.NotaStockInicialGuardarView.as_view(), name='nota_stock_inicial_guardar'),
    path('nota-stock-inicial/anular/<pk>/', views.NotaStockInicialAnularView.as_view(), name='nota_stock_inicial_anular'),
    
    path('nota-stock-inicial/generar-nota-ingreso/<int:pk>/', views.NotaStockInicialGenerarNotaIngresoView.as_view(), name='nota_stock_inicial_generar_nota_ingreso'),

]