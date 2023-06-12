from django.urls import path
from . import views

app_name = 'recepcion_compra_app'

urlpatterns = [

    path('recepcion-compra/detalle/<pk>/', views.RecepcionCompraDetailView.as_view(), name='recepcion_compra_detalle'),
    path('recepcion-compra/detalle/tabla/<pk>/', views.RecepcionCompraDetailTabla, name='recepcion_compra_detalle_tabla'),
    path('recepcion-compra/anular/<pk>/', views.RecepcionCompraAnularView.as_view(), name='recepcion_compra_anular'),

    path('archivo-recepcion-compra/crear/<pk>/', views.ArchivoRecepcionCompraCreateView.as_view(), name='archivo_recepcion_compra_crear'),
    path('archivo-recepcion-compra/eliminar/<pk>/', views.ArchivoRecepcionCompraDeleteView.as_view(), name='archivo_recepcion_compra_eliminar'),
    
    path('foto-recepcion-compra/crear/<pk>/', views.FotoRecepcionCompraCreateView.as_view(), name='foto_recepcion_compra_crear'),
    path('foto-recepcion-compra/eliminar/<pk>/', views.FotoRecepcionCompraDeleteView.as_view(), name='foto_recepcion_compra_eliminar'),
    
    path('recepcion-compra/generar-nota-ingreso/<pk>/', views.RecepcionCompraGenerarNotaIngresoView.as_view(), name='recepcion_compra_generar_nota_credito'),
    
    path('recepcion-compra/generar-documento-reclamo/<pk>/', views.RecepcionCompraGenerarDocumentoReclamoView.as_view(), name='recepcion_compra_generar_documento_reclamo'),
    
    path('documento-reclamo/lista/<id_recepcion>/', views.DocumentoReclamoListView.as_view(), name='documento_reclamo_lista'),
    path('documento-reclamo/detalle/<pk>/', views.DocumentoReclamoDetailView.as_view(), name='documento_reclamo_detalle'),
    path('documento-reclamo/detalle/tabla/<pk>/', views.DocumentoReclamoDetailTabla, name='documento_reclamo_detalle_tabla'),
    path('documento-reclamo/eliminar/<pk>/', views.DocumentoReclamoDeleteView.as_view(), name='documento_reclamo_eliminar'),
    path('documento-reclamo/confirmar/<pk>/', views.DocumentoReclamoConfirmarView.as_view(), name='documento_reclamo_confirmar'),
    path('documento-reclamo/confirmar/revertir/<pk>/', views.DocumentoReclamoConfirmarRevertirView.as_view(), name='documento_reclamo_confirmar_revertir'),
    path('documento-reclamo/finalizar/<pk>/', views.DocumentoReclamoFinalizarView.as_view(), name='documento_reclamo_finalizar'),
    path('documento-reclamo/finalizar/revertir/<pk>/', views.DocumentoReclamoFinalizarRevertirView.as_view(), name='documento_reclamo_finalizar_revertir'),
    
    path('documento-reclamo/detalle/actualizar/<pk>/', views.DocumentoReclamoDetalleUpdateView.as_view(), name='documento_reclamo_detalle_actualizar'),
    path('documento-reclamo/detalle/actualizar/monto/<pk>/', views.DocumentoReclamoDetalleMontoUpdateView.as_view(), name='documento_reclamo_detalle_actualizar_monto'),
]